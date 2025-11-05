class APIClient {
    constructor(baseURL = 'http://127.0.0.1:5000/api') {
        this.baseURL = baseURL;
    }

    async scanImage(imageFile, options = {}) {
        const formData = new FormData();
        formData.append('image', imageFile);

        if (options.advancedDetection) {
            formData.append('advanced_detection', 'true');
        }

        const response = await fetch(`${this.baseURL}/scan`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro no servidor');
        }

        return await response.json();
    }

    async generateDecklist(imageFile, outputName, options = {}) {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('output_name', outputName);

        if (options.advancedDetection) {
            formData.append('advanced_detection', 'true');
        }

        const response = await fetch(`${this.baseURL}/generate-decklist`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro no servidor');
        }

        return await response.blob();
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}
