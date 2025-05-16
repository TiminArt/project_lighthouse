// Для объектов недвижимости
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    
    if (filterForm) {
        // Обработка изменения фильтров
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyFilters();
        });
        
        // Инициализация фильтров из URL
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.toString()) {
            applyFilters();
        }
    }
    
    function applyFilters() {
        const formData = new FormData(document.getElementById('filter-form'));
        const params = new URLSearchParams(formData);
        
        // Обновляем URL без перезагрузки страницы
        window.history.pushState({}, '', `${window.location.pathname}?${params.toString()}`);
        
        // AJAX запрос
        fetch(`?${params.toString()}&ajax=1`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById('property-results').innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
    }
});
// Инициализация Lightbox для динамически загружаемых изображений
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lightbox !== 'undefined') {
        lightbox.init();
    }
});