ymaps.ready(init);
        function init() {
            var myMap = new ymaps.Map("yandex-map", {
                center: [55.900172, 38.065863],
                zoom: 16,
                controls: ['zoomControl', 'fullscreenControl']
            });

            var myPlacemark = new ymaps.Placemark([55.900172, 38.065863], {
                hintContent: 'Агентство недвижимости',
                balloonContent: 'г. Щёлково-3, ул. Радиоцентра № 5, 16'
            }, {
                preset: 'islands#icon',
                iconColor: '#BFA315'
            });

            myMap.geoObjects.add(myPlacemark);
        }