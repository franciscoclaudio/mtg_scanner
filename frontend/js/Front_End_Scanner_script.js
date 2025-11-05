import { APIClient } from './modules/api-client.js';
import { UIManager } from './modules/ui-manager.js';
import { ImagePreview } from './modules/image-preview.js';

class MTGScanner {
    constructor() {
        this.apiClient = new APIClient();
        this.uiManager = new UIManager();
        this.imagePreview = new ImagePreview();
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const form = document.getElementById('scannerForm');
        const imageInput = document.getElementById('img');
        const nameOutputInput = document.getElementById('NameOutput');

        // Preview de imagem
        imageInput.addEventListener('change', (e) => {
            this.imagePreview.handleImageSelect(e);
        });

        // Geração automática de nome de arquivo
        imageInput.addEventListener('change', () => {
            this.generateOutputFilename(nameOutputInput);
        });

        // Submissão do formulário
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });

        // Verificação de saúde da API
        this.checkAPIHealth();
    }

    generateOutputFilename(nameOutputInput) {
        const imageInput = document.getElementById('img');
        if (imageInput.files.length === 0) return;

        const file = imageInput.files[0];
        let baseName = file.name.replace(/\.[^/.]+$/, ""); // Remove extensão
        nameOutputInput.value = `${baseName}_decklist.txt`;
    }

    async handleFormSubmit() {
        const imageInput = document.getElementById('img');
        const nameOutputInput = document.getElementById('NameOutput');
        const submitButton = document.getElementById('submitButton');
        const advancedDetection = document.getElementById('advancedDetection');

        // Validação
        if (imageInput.files.length === 0) {
            this.uiManager.showStatus('❌ Por favor, selecione uma imagem.', 'error');
            return;
        }

        const file = imageInput.files[0];
        let outputFilename = nameOutputInput.value.trim();

        // Validação do nome de arquivo
        if (!outputFilename.toLowerCase().endsWith('.txt')) {
            outputFilename += '.txt';
            nameOutputInput.value = outputFilename;
        }

        try {
            this.uiManager.showLoading(submitButton);
            this.uiManager.showStatus('⏳ Processando imagem...', 'loading');

            const options = {
                advancedDetection: advancedDetection?.checked || false
            };

            // Gera decklist e faz download
            const blob = await this.apiClient.generateDecklist(file, outputFilename, options);
            this.uiManager.triggerDownload(blob, outputFilename);
            
            this.uiManager.showStatus('✅ Decklist gerado com sucesso!', 'success');

        } catch (error) {
            console.error('Erro:', error);
            this.uiManager.showStatus(`❌ ${error.message}`, 'error');
        } finally {
            this.uiManager.hideLoading(submitButton);
        }
    }

    async checkAPIHealth() {
        const isHealthy = await this.apiClient.healthCheck();
        if (!isHealthy) {
            this.uiManager.showStatus(
                '⚠️ Servidor não está respondendo. Certifique-se de que o backend está rodando.',
                'error'
            );
        }
    }
}

// Inicializa a aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new MTGScanner();
});
