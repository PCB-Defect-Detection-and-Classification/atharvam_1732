import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import os
from src import config

@st.cache_resource
def load_defect_model():
    if not os.path.exists(config.MODEL_PATH):
        st.error(f"❌ Error: Model not found at {config.MODEL_PATH}")
        return None
    try:
        model = tf.keras.models.load_model(config.MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def smart_align(img_test, img_temp):
    gray_test = cv2.cvtColor(img_test, cv2.COLOR_RGB2GRAY)
    gray_temp = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY) 
    
    if len(img_temp.shape) == 3 and img_temp.shape[2] == 3:
         gray_temp = cv2.cvtColor(img_temp, cv2.COLOR_RGB2GRAY)
    
    orb = cv2.ORB_create(MAX_FEATURES=2000)
    kp1, des1 = orb.detectAndCompute(gray_test, None)
    kp2, des2 = orb.detectAndCompute(gray_temp, None)
    
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = sorted(matches, key=lambda x: x.distance)
    matches = matches[:int(len(matches) * 0.25)]
    
    pts1 = np.zeros((len(matches), 2), dtype=np.float32)
    pts2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        pts1[i, :] = kp1[match.queryIdx].pt
        pts2[i, :] = kp2[match.trainIdx].pt
    
    h, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC)
    h_img, w_img = img_temp.shape[:2]
    img_aligned = cv2.warpPerspective(img_test, h, (w_img, h_img))
    return img_aligned

def run_inspection(template_img, test_img, model, confidence_threshold=50):
    try:
        aligned_test = smart_align(test_img, template_img)
    except:
        aligned_test = cv2.resize(test_img, (template_img.shape[1], template_img.shape[0]))

    blur_test = cv2.GaussianBlur(aligned_test, (3,3), 0)
    blur_temp = cv2.GaussianBlur(template_img, (3,3), 0)
    
    diff = cv2.absdiff(blur_temp, blur_test)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2) 
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    annotated_img = aligned_test.copy()
    defects_found = []
    
    img_h, img_w = aligned_test.shape[:2]
    class_names = ['Missing Hole', 'Mouse Bite', 'Open Circuit', 'Short', 'Spur', 'Spurious Copper']
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w * h > 20:
            vis_pad = 5
            vx1 = max(0, x - vis_pad)
            vy1 = max(0, y - vis_pad)
            vx2 = min(img_w, x + w + vis_pad)
            vy2 = min(img_h, y + h + vis_pad)
            
            ai_pad = 20 
            ax1 = max(0, x - ai_pad)
            ay1 = max(0, y - ai_pad)
            ax2 = min(img_w, x + w + ai_pad)
            ay2 = min(img_h, y + h + ai_pad)
            
            roi_ai = aligned_test[ay1:ay2, ax1:ax2]
            if roi_ai.size == 0: continue
            
            roi_resized = cv2.resize(roi_ai, config.IMG_SIZE)
            roi_batch = np.expand_dims(roi_resized, axis=0)
            
            preds = model.predict(roi_batch, verbose=0)
            score = np.max(preds) * 100
            label_idx = np.argmax(preds)
            label = class_names[label_idx]
            
            if score >= confidence_threshold:
                color = (0, 0, 255) 
                cv2.rectangle(annotated_img, (vx1, vy1), (vx2, vy2), color, 2)
                
                font_scale = 0.4 if w*h > 500 else 0.3
                cv2.putText(annotated_img, f"{label} {int(score)}%", (vx1, vy1-3), 
                           cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 1)
                
                defects_found.append({"type": label, "confidence": score, "bbox": [vx1, vy1, vx2, vy2]})
                
    return aligned_test, annotated_img, defects_found