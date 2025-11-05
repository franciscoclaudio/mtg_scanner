from flask import Blueprint, request, jsonify
from ..services.scryfall_api import ScryfallService

cards_bp = Blueprint('cards', __name__)
scryfall_service = ScryfallService()

@cards_bp.route('/search/<card_name>', methods=['GET'])
def search_card(card_name):
    """Busca uma carta específica pelo nome"""
    try:
        card_data = scryfall_service.search_card_by_name(card_name, exact=False)
        if card_data:
            return jsonify({
                'success': True,
                'card': scryfall_service._format_card_data(card_data)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Carta não encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@cards_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'MTG Scanner API está funcionando',
        'service': 'cards'
    })
