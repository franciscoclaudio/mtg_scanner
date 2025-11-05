import cv2
import numpy as np
from PIL import Image
import pytesseract
from ...utils.config import Config

class ImageProcessor:
    def __init__(self):
        self.tesseract_cmd = Config.TESSERACT_CMD
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
    
    def preprocess_image(self, image):
        """Preprocessa imagem para melhorar OCR"""
        if isinstance(image, Image.Image):
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            image_cv = image.copy()
        
        # Converte para escala de cinza
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        
        # Redução de ruído
        denoised = cv2.medianBlur(gray, 3)
        
        # Equalização de histograma
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        equalized = clahe.apply(denoised)
        
        # Threshold adaptativo
        thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        return thresh
    
    def extract_text(self, image):
        """Extrai texto da imagem usando OCR"""
        try:
            processed_image = self.preprocess_image(image)
            
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\ \-.,'
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            return text.strip()
            
        except Exception as e:
            print(f"Erro no OCR: {e}")
            return ""
    
    def detect_card_contours(self, image):
        """Detecta contornos de cartas na imagem"""
        try:
            if isinstance(image, Image.Image):
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                image_cv = image.copy()
            
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            card_regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 10000:  # Filtra por área mínima
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    if len(approx) == 4:  # Retângulo (carta)
                        x, y, w, h = cv2.boundingRect(contour)
                        card_regions.append((x, y, w, h))
            
            return card_regions
            
        except Exception as e:
            print(f"Erro na detecção de contornos: {e}")
            return []
