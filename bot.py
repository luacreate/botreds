<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1Win Access</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: url('redsoftlogo.png') no-repeat center center;
            background-size: cover;
            overflow: hidden;
            font-family: 'Poppins', sans-serif;
            color: white;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 15px;
            border-radius: 15px;
            background: rgba(40, 40, 60, 0.8);
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        .accuracy-message {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
        }

        .logo {
            width: 80px;
            margin-bottom: 15px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 15px;
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .multiplier-container {
            position: relative;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            margin: 30px 0;
            width: 120px;
            height: 120px;
        }

        .multiplier-circle {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px dashed rgba(0, 212, 255, 0.7);
            animation: spin 8s linear infinite;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .multiplier {
            font-size: 2.5em;
            color: #00ffcc;
            text-shadow: 0 0 15px rgba(0, 255, 204, 0.7);
        }

        .button {
            padding: 12px 30px;
            font-size: 1.2em;
            margin: 15px;
            cursor: pointer;
            background: linear-gradient(to right, #FFD700, #FFA500);
            border: none;
            border-radius: 10px;
            color: white;
            transition: background 0.4s, transform 0.3s;
        }

        .button:hover {
            background: linear-gradient(to right, #FFA500, #FFD700);
        }

        .support {
            position: fixed;
            bottom: 15px;
            background: rgba(50, 50, 50, 0.7);
            padding: 8px;
            border-radius: 8px;
        }

        .support a {
            color: #ff8bff;
            text-decoration: none;
        }

        .support a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container" id="mainContainer">
        <!-- Сообщение о точности сигналов -->
        <div class="accuracy-message" id="accuracyMessage" style="display: none;"></div>
        
        <img src="https://1winbd.com/wp-content/uploads/2022/10/lucky-jet-header.webp" alt="Логотип" class="logo" />
        <h1>Red Soft Signals</h1>

        <div class="multiplier-container">
            <div class="multiplier-circle"></div>
            <div class="multiplier" id="multiplier">x0.00</div>
        </div>

        <button class="button" onclick="checkDepositAndGenerateSignal()">Получить сигнал</button>
        <button class="button" onclick="window.location.href='menu.html'">Вернуться в меню</button>
    </div>

    <div class="support">
        Тех. Поддержка: <a href="https://t.me/redsoft_support" target="_blank">Написать в Telegram</a>
    </div>

    <script>
        // Функция для проверки депозита и генерации множителя
        function checkDepositAndGenerateSignal() {
            const userId = localStorage.getItem('userId');
            const multiplierElement = document.getElementById("multiplier");

            if (!userId) {
                alert("Ошибка: ID пользователя не найден!");
                return;
            }

            // Проверка депозита на сервере
            fetch('https://postback-server-boba.onrender.com/data')
                .then(response => response.json())
                .then(data => {
                    const userEntry = data.find(entry => entry.user_id === userId);

                    if (userEntry) {
                        if (userEntry.amount > 19) {
                            displayAccuracyMessage(userEntry.amount);
                            generateRandomMultiplier();
                        } else {
                            showConnectingMessage();
                        }
                    } else {
                        alert("Аккаунт не найден!");
                    }
                })
                .catch(error => {
                    console.error('Ошибка при проверке аккаунта:', error);
                    alert("Ошибка сервера. Попробуйте позже.");
                });
        }

        // Функция отображения сообщения о точности сигналов
        function displayAccuracyMessage(depositAmount) {
            const accuracyMessageElement = document.getElementById('accuracyMessage');
            const accuracy = Math.min(depositAmount, 99); // Ограничим точность до 99%
            accuracyMessageElement.textContent = `Точность сигналов для вашего аккаунта: ${accuracy}%`;
            accuracyMessageElement.style.display = 'block';
        }

        // Функция для отображения сообщения и перенаправления на страницу error.html
        function showConnectingMessage() {
            const container = document.getElementById("mainContainer");
            const messageElement = document.createElement('p');
            messageElement.textContent = "Подключение к серверу...";
            messageElement.id = 'connectingMessage';
            container.appendChild(messageElement);

            setTimeout(() => {
                window.location.href = 'error.html';
            }, 4000);
        }

        // Функция генерации случайного множителя
        function generateRandomMultiplier() {
            const multiplierElement = document.getElementById("multiplier");
            setTimeout(() => {
                const randomMultiplier = (Math.random() * 9 + 1).toFixed(2);
                multiplierElement.textContent = `x${randomMultiplier}`;
            }, 2000);
        }
    </script>
</body>
</html>
