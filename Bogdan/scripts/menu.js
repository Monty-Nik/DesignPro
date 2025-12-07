// 1. Находим элементы
const jsButton = document.querySelector('.jsButtonMainMenu');
const mainMenu = document.querySelector('.main_menu');

// 2. Проверяем, что оба элемента найдены (защита от ошибок)
if (jsButton && mainMenu) {
    // 3. Вешаем обработчик на КОРРЕКТНУЮ переменную — jsButton
    jsButton.addEventListener('click', () => {
        mainMenu.classList.toggle('jsMenuVisually');
    });
}