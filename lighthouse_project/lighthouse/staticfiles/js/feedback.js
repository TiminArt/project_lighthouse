// feedback.js - Обработка формы обратной связи
(function() {
    // Защита от повторной инициализации
    if (window.feedbackFormHandlerLoaded) return;
    window.feedbackFormHandlerLoaded = true;
    
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('feedbackForm');
        if (!form) return;

        // Локальные переменные
        let isSubmitting = false;
        const alertBox = document.getElementById('feedbackAlert');
        const phoneInput = document.getElementById('phone');
        const messageInput = document.getElementById('message');
        const submitBtn = form.querySelector('.submit-btn');
        
        // if (!phoneInput || !messageInput || !submitBtn || !alertBox) {
        //     console.error('Один из обязательных элементов формы не найден');
        //     return;
        // }

        // Валидация сообщения
        messageInput.addEventListener('input', function() {
            this.value = this.value.trimStart();
            const minLength = 10;
            const currentLength = this.value.length;
            
            if (currentLength < minLength && currentLength > 0) {
                this.setCustomValidity(`Минимум ${minLength} символов (осталось ${minLength - currentLength})`);
            } else {
                this.setCustomValidity('');
            }
            
            const counter = document.getElementById('messageCounter');
            if (counter) {
                counter.textContent = `${currentLength}/${minLength}`;
                counter.style.color = currentLength >= minLength ? 'green' : 'red';
            }
        });

        // Обработка отправки
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            if (isSubmitting) return;
            isSubmitting = true;

            if (!form.checkValidity()) {
                form.reportValidity();
                isSubmitting = false;
                return;
            }

            const btnText = submitBtn.querySelector('.btn-text');
            const loader = submitBtn.querySelector('.loader');
            
            try {
                submitBtn.disabled = true;
                if (btnText) btnText.style.opacity = '0.5';
                if (loader) loader.style.display = 'block';

                const formData = new FormData(form);
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                
                if (!csrfToken) throw new Error('CSRF token not found');

                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                
                const data = await response.json();
                showAlert(data.message || (data.status === 'success' ? 'Успешно отправлено!' : 'Ошибка'), 
                          data.status === 'success' ? 'success' : 'error');
                
                if (data.status === 'success') form.reset();

            } catch (error) {
                console.error('Ошибка:', error);
                showAlert(error.message.includes('CSRF') ? 
                    'Ошибка безопасности. Обновите страницу' : 
                    'Ошибка соединения с сервером', 'error');
            } finally {
                isSubmitting = false;
                submitBtn.disabled = false;
                if (btnText) btnText.style.opacity = '1';
                if (loader) loader.style.display = 'none';
            }
        });

        function showAlert(message, type = 'success') {
            alertBox.textContent = message;
            alertBox.className = `alert alert-${type}`;
            alertBox.style.display = 'block';
            alertBox.style.opacity = '0';
            alertBox.style.transform = 'translateY(-20px)';
            
            requestAnimationFrame(() => {
                alertBox.style.transition = 'all 0.3s ease';
                alertBox.style.opacity = '1';
                alertBox.style.transform = 'translateY(0)';
            });

            setTimeout(() => {
                alertBox.style.opacity = '0';
                alertBox.style.transform = 'translateY(-20px)';
                setTimeout(() => alertBox.style.display = 'none', 300);
            }, 5000);
        }
    });
})();