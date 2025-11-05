class ImagePreview {
    constructor() {
        this.previewContainer = document.getElementById('previewContainer');
        this.imagePreview = document.getElementById('imagePreview');
    }

    handleImageSelect(event) {
        const file = event.target.files[0];
        
        if (file) {
            // Verifica se é uma imagem
            if (!file.type.match('image.*')) {
                this.hidePreview();
                return;
            }

            const reader = new FileReader();
            
            reader.onload = (e) => {
                this.imagePreview.src = e.target.result;
                this.showPreview();
            };
            
            reader.readAsDataURL(file);
        } else {
            this.hidePreview();
        }
    }

    showPreview() {
        this.previewContainer.classList.remove('hidden');
        this.imagePreview.classList.remove('hidden');
    }

    hidePreview() {
        this.previewContainer.classList.add('hidden');
        this.imagePreview.classList.add('hidden');
    }

    clearPreview() {
        this.imagePreview.src = '';
        this.hidePreview();
    }
}

export { ImagePreview };
