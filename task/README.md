my-app
Project setup
В начале убедитесь, что Node.js и npm установлены:

node -v
npm -v
Если нет этого, то пропишите команду:

npm install
Скопируйте ссылку репозитория, клонируйте, откройте проект:

git clone https://github.com/Vasilisa321/Task4.git
cd Task4
Перейдите на ветку "1":

git checkout 1
Compiles and hot-reloads for development
Зайдите в my-app (должно быть ...\4\my-app>):

cd my-app
Запустите сервер разработки:

npm run serve
При запуске в терминале должно быть:

App running at:
- Local:   http://localhost:8080/ Перейдите по этому адресу
- Network: http://192.168.13.19:8080/
  Compiles and minifies for production
  npm run build
  Customize configuration
  See Configuration Reference.