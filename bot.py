<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Soft Signals</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: url('redsoftlogo.png') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Poppins', sans-serif;
            color: #fff;
            overflow: hidden;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
            border-radius: 20px;
            background: rgba(0, 0, 0, 0.6);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            width: 90%;
            max-width: 400px;
        }

        .logo {
            width: 120px;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .accuracy-message {
            font-size: 1.2em;
            margin-bottom: 20px;
            color: #FFD700;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }

        .multiplier-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: rgba(255, 50, 50, 0.2);
            box-shadow: 0 4px 15px rgba(255, 0, 0, 0.5);
        }

        .multiplier {
            font-size: 2em;
            font-weight: bold;
            color: #ff6f61;
        }

        #entroImage {
            display: none;
            width: 100%;
            height: auto;
        }

        .button {
            padding: 15px;
            margin-top: 20px;
            width: 100%;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .button:hover {
            transform: translateY(-3px);
        }

        .support {
            margin-top: 20px;
            font-size: 0.9em;
        }

        .support a {
            color: #ff8bff;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://1winbd.com/wp-content/uploads/2022/10/lucky-jet-header.webp" alt="Логотип" class="logo">
        <h1>Red Soft Signals</h1>

        <!-- Сообщение о точности сигналов -->
        <div class="accuracy-message" id="accuracyMessage"></div>

        <!-- Множитель или изображение -->
        <div class="multiplier-container">
            <img src="entro.svg" alt="Загрузка" id="entroImage">
            <div class="multiplier" id="multiplier">x0.00</div>
        </div>

        <button class="button" onclick="checkDepositAndGenerateSignal()">Получить сигнал</button>
        <button class="button secondary" onclick="window.location.href='menu.html'">Вернуться в меню</button>

        <div class="support">
            Тех. Поддержка: <a href="https://t.me/redsoft_support" target="_blank">Написать в Telegram</a>
        </div>
    </div>

    <script>
        const multiplierElement = document.getElementById("multiplier");
        const entroImage = document.getElementById("entroImage");
        const accuracyMessageElement = document.getElementById("accuracyMessage");

        // Функция инициализации
        function init() {
            multiplierElement.style.display = 'none';
            entroImage.style.display = 'block';
        }

        // Функция проверки депозита и генерации множителя
        function checkDepositAndGenerateSignal() {
            const userId = localStorage.getItem('userId');
            if (!userId) {
                alert("Ошибка: ID пользователя не найден!");
                return;
            }

            fetch('https://postback-server-boba.onrender.com/data')
                .then(response => response.json())
                .then(data => {
                    const userEntry = data.find(entry => entry.user_id === userId);
                    if (userEntry) {
                        if (userEntry.amount > 19) {
                            displayAccuracyMessage(userEntry.amount);
                            displayLoadingAndGenerateMultiplier();
                        } else {
                            alert("Недостаточно депозита для сигнала.");
                        }
                    } else {
                        alert("Аккаунт не найден!");
                    }
                })
                .catch(error => {
                    console.error('Ошибка сервера:', error);
                });
        }

        // Функция отображения точности сигналов
        function displayAccuracyMessage(depositAmount) {
            const accuracy = Math.min(depositAmount, 99); // Ограничиваем до 99%
            accuracyMessageElement.textContent = `Точность сигналов для вашего аккаунта: ${accuracy}%`;
            accuracyMessageElement.style.opacity = '1';
        }

        // Функция отображения `entro.svg` и генерации множителя
        function displayLoadingAndGenerateMultiplier() {
            multiplierElement.style.display = 'none';
            entroImage.style.display = 'block';
            
            setTimeout(() => {
                entroImage.style.display = 'none';
                const randomMultiplier = (Math.random() * 9 + 1).toFixed(2);
                multiplierElement.textContent = `x${randomMultiplier}`;
                multiplierElement.style.display = 'block';
                multiplierElement.classList.add("animate-multiplier");
                setTimeout(() => {
                    multiplierElement.classList.remove("animate-multiplier");
                }, 1000);
            }, 4000);
        }

        // Инициализация при загрузке страницы
        window.onload = init;
    </script>
</body>
</html>
