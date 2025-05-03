import cv2
import numpy as np

def simulate_glaucoma(frame, severity=0.5):
    if severity <= 0:
        return frame
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    visible_radius_ratio = 0.25 + (1 - severity) * 0.25
    transition_ratio = 0.15
    mask_blur_ksize = 151
    visible_radius = int(min(h, w) * visible_radius_ratio)
    max_radius = visible_radius + int(min(h, w) * transition_ratio)
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    mask = np.clip((max_radius - dist) / (max_radius - visible_radius), 0, 1)
    mask = cv2.GaussianBlur(mask.astype(np.float32), (mask_blur_ksize, mask_blur_ksize), 0)
    mask = np.clip(mask, 0, 1)
    mask = np.expand_dims(mask, axis=2)
    output = (frame * mask).astype(np.uint8)
    cv2.putText(output, "Glaucoma", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)
    return output

def simulate_cataract_yellow(frame, severity=0.5):
    if severity <= 0:
        return frame
    yellow_tint = np.full_like(frame, (0, 255, 255))
    alpha = 0.2 * severity
    return cv2.addWeighted(frame, 1 - alpha, yellow_tint, alpha, 0)

def simulate_cataract_blur(frame, severity=0.5):
    if severity <= 0:
        return frame
    h, w = frame.shape[:2]
    blur_strength = int(25 + 40 * severity) | 1
    blurred = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
    Y, X = np.ogrid[:h, :w]
    cx, cy = w // 2, h // 2
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_r = 0.5 * min(h, w)
    mask = np.clip((max_r - dist) / max_r, 0, 1)
    mask = cv2.GaussianBlur(mask.astype(np.float32), (151, 151), 0)
    mask = np.expand_dims(mask, 2)
    haze = np.full_like(frame, 255)
    output = (blurred * (1 - mask * severity) + haze * mask * severity).astype(np.uint8)
    return output

def generate_retinopathy_mask(height, width, num_spots):
    mask = np.zeros((height, width), dtype=np.uint8)
    for _ in range(num_spots):
        center = (np.random.randint(0, width), np.random.randint(0, height))
        axes = (np.random.randint(20, 70), np.random.randint(10, 50))
        angle = np.random.randint(0, 360)
        cv2.ellipse(mask, center, axes, angle, 0, 360, 255, -1)
    return mask

def simulate_retinopathy(frame, severity=0.5, static_mask=[None]):
    if severity <= 0:
        return frame
    h, w = frame.shape[:2]
    base_spots = 8
    max_spots = 20
    max_opacity = 0.8
    num_spots = int(base_spots + (max_spots - base_spots) * severity)
    if static_mask[0] is None or static_mask[0].shape != (h, w):
        static_mask[0] = generate_retinopathy_mask(h, w, num_spots)
    alpha = (static_mask[0].astype(np.float32) / 255.0) * (0.3 + severity * (max_opacity - 0.3))
    alpha = np.expand_dims(alpha, axis=2)
    output = (frame.astype(np.float32) * (1 - alpha)).astype(np.uint8)
    cv2.putText(output, "Diabetic Retinopathy", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    return output

def simulate_macular_degeneration(frame, severity=0.5):
    if severity <= 0:
        return frame
    h, w = frame.shape[:2]
    Y, X = np.ogrid[:h, :w]
    center_x = int(w * (0.5 - 0.2 * severity))
    center_y = h // 2
    max_radius = np.sqrt(h**2 + w**2)
    radius = int((0.3 + 0.7 * severity) * min(h, w))
    feather = int(0.4 * radius)
    dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    mask = np.zeros((h, w), dtype=np.float32)
    inside = dist <= radius
    feather_region = (dist > radius) & (dist <= radius + feather)
    mask[inside] = 1.0
    mask[feather_region] = 1 - (dist[feather_region] - radius) / feather
    if severity >= 1.0:
        mask[:, :] = 1.0
    mask = np.expand_dims(mask, axis=2)
    output = (frame * (1 - mask)).astype(np.uint8)
    cv2.putText(output, "Macular Degeneration", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)
    return output
