from config import SSIM_THRESHOLD, L2_RANGE
import numpy as np
from skimage.metrics import structural_similarity as ssim

def get_distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def get_ssim(img_array, m_img_array, data_range=255):
    return ssim(img_array, m_img_array, data_range=data_range) * 100

def convert_to_grayscale(img_array):
    weights = np.array([0.2989, 0.5870, 0.1140])
    return np.dot(img_array[..., :3], weights)

def validate_mutation(img_array, m_img_array):
    """
    Check if the mutation is valid based on L2 distance and SSIM constraints.
    """
    if img_array.shape[2] == 3:
        img_array = convert_to_grayscale(img_array)
        m_img_array = convert_to_grayscale(m_img_array)

    img_l2 = np.linalg.norm(img_array)
    m_img_l2 = np.linalg.norm(m_img_array)
    distance = np.linalg.norm(img_array - m_img_array)
    ssi = ssim(img_array, m_img_array, data_range=255)

    valid_mutation = (
        0 < distance < img_l2 * (1 + L2_RANGE) and
        ssi >= SSIM_THRESHOLD
    )
    return valid_mutation, ssi, distance, img_l2, m_img_l2
