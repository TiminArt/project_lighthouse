document.addEventListener('DOMContentLoaded', function () {
    // МОДАЛЬНОЕ ОКНО
    const modal = document.getElementById('feedbackModal');
    const requestBtn = document.querySelector('.request-btn');
    const closeBtn = document.querySelector('.close-btn');

    requestBtn.addEventListener('click', function () {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    });

    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // БУРГЕР-МЕНЮ
    const burgerBtn = document.querySelector('.burger-btn');
    const navigation = document.querySelector('.navigation');
    const overlay = document.querySelector('.overlay');

    burgerBtn.addEventListener('click', function () {
        this.classList.toggle('active');
        navigation.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    });

    overlay.addEventListener('click', function () {
        burgerBtn.classList.remove('active');
        navigation.classList.remove('active');
        this.classList.remove('active');
        document.body.classList.remove('no-scroll');
    });

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function () {
            burgerBtn.classList.remove('active');
            navigation.classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('no-scroll');
        });
    });

    // УВЕДОМЛЕНИЯ
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.classList.add('notification', type);
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }

    // СТИЛИ УВЕДОМЛЕНИЙ
    const notificationStyles = document.createElement('style');
    notificationStyles.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            z-index: 10000;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            opacity: 0;
            transform: translateY(-20px);
            animation: fadeIn 0.3s ease-out forwards;
        }
        .notification.success {
            background-color: #4CAF50;
        }
        .notification.error {
            background-color: #f44336;
        }
        .notification.fade-out {
            animation: fadeOut 0.5s ease-out forwards;
        }
        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeOut {
            to {
                opacity: 0;
                transform: translateY(-20px);
            }
        }
    `;
    document.head.appendChild(notificationStyles);

    // ОБРАБОТКА ФОРМЫ ОБРАТНОЙ СВЯЗИ
    const feedbackForm = document.getElementById('feedbackForm');

    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(feedbackForm);

            fetch(feedbackForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    feedbackForm.reset();
                    showNotification('Заявка успешно отправлена!', 'success');
                } else {
                    return response.text().then(text => {
                        throw new Error(text);
                    });
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке формы:', error);
                showNotification('Произошла ошибка. Попробуйте ещё раз.', 'error');
            });
        });
    }
});
