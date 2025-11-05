from flask import Blueprint, request, jsonify, send_file
import io
from PIL import Image
from ..services.image_processing import ImageProcessor
from ..services.scryfall_api import ScryfallService

scanner_bp = Blueprint('scanner', __name__)
image_processor = ImageProcessor()
scryfall_service = ScryfallService()

@scanner_bp.route('/scan', methods=['POST'])
def scan_image():
    """Endpoint principal para escanear imagem"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem fornecida'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Processa imagem
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Extrai texto
        extracted_text = image_processor.extract_text(image)
        
        if not extracted_text:
            return jsonify({
                'error': 'Não foi possível extrair texto da imagem',
                'suggestion': 'Tente uma imagem com melhor qualidade e iluminação'
            }), 400
        
        # Busca cartas no Scryfall
        detected_cards = scryfall_service.search_cards_by_text(extracted_text)
        
        return jsonify({
            'success': True,
            'cards_detected': len(detected_cards),
            'extracted_text': extracted_text,
            'cards': detected_cards
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@scanner_bp.route('/generate-decklist', methods=['POST'])
def generate_decklist():
    """Gera arquivo de decklist para download"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem fornecida'}), 400
        
        file = request.files['image']
        output_name = request.form.get('output_name', 'decklist.txt')
        
        # Processa imagem (similar ao endpoint /scan)
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        extracted_text = image_processor.extract_text(image)
        detected_cards = scryfall_service.search_cards_by_text(extracted_text)
        
        if not detected_cards:
            return jsonify({
                'error': 'Nenhuma carta identificada',
                'cards_detected': 0
            }), 400
        
        # Gera conteúdo do decklist
        decklist_content = _create_decklist_content(detected_cards)
        
        # Salva arquivo temporário
        temp_filename = f"temp_{output_name}"
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(decklist_content)
        
        return send_file(
            temp_filename,
            as_attachment=True,
            download_name=output_name,
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

def _create_decklist_content(cards):
    """Cria conteúdo formatado do decklist"""
    from datetime import datetime
    
    card_counts = {}
    for card in cards:
        card_name = card['name']
        card_counts[card_name] = card_counts.get(card_name, 0) + 1
    
    content = "MTG Decklist - Gerado por Scanner\n"
    content += "=" * 50 + "\n\n"
    
    for card_name, count in sorted(card_counts.items()):
        content += f"{count} {card_name}\n"
    
    content += f"\nTotal: {sum(card_counts.values())} cartas"
    content += f"\nGerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    return content
