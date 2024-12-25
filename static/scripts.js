// function markCorrectAnswer(questionId, answerId) {
//     fetch('/answer/mark_correct/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken'),
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         body: new URLSearchParams({
//             question_id: questionId,
//             answer_id: answerId,
//         }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             document.querySelectorAll('.correct-answer-indicator').forEach(el => el.classList.remove('correct'));
//
//             const selectedIndicator = document.querySelector(`#answer-${data.correct_answer_id} .correct-answer-indicator`);
//             if (selectedIndicator) {
//                 selectedIndicator.classList.add('correct');
//             }
//         } else {
//             alert(data.error || 'An error occurred.');
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

document.addEventListener('DOMContentLoaded', function () {
    const markCorrectButtons = document.querySelectorAll('.mark-correct-btn');

    markCorrectButtons.forEach(button => {
        button.addEventListener('click', function () {
            const answerId = this.dataset.id;
            const questionId = this.dataset.question;

            const csrfToken = getCookie('csrftoken'); // Убедитесь, что функция getCookie определена.

            // Отправка AJAX-запроса
            fetch('/answer/mark_correct/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    question_id: questionId,
                    answer_id: answerId,
                }),
            })
                .then(response => response.json())
                // .then(response => {
                //     if (!response.ok) {
                //         throw new Error(`HTTP error! status: ${response.status}`);
                //     }
                //     return response.json();
                // })
                .then(data => {
                    // Успешный ответ от сервера
                    if (data.success) {
                        // Очистить все предыдущие отметки "Correct answer!"
                        document.querySelectorAll('[id^="correct-answer-"]').forEach(el => {
                            el.innerHTML = '';
                        });

                        // Добавить отметку к текущему ответу
                        const correctAnswerElement = document.getElementById(`correct-answer-${answerId}`);
                        if (correctAnswerElement) {
                            correctAnswerElement.innerHTML = `
                                <i class="bi bi-check2-square"></i>Correct answer!
                            `;
                        }
                    } else {
                        console.error('Error marking correct answer:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});

document.querySelectorAll('.vote-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.dataset.id;
        const type = this.dataset.type;
        const action = this.dataset.action;
        const isNegative = action === 'dislike';
        const url = type === 'question' ? '/question/vote/' : '/answer/vote/';
        const target = type === 'question' ? `#question-votes-${id}` : `#answer-votes-${id}`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                [`${type}_id`]: id,
                is_negative: isNegative,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector(target).textContent = data.total_votes;
            } else {
                alert(data.error || 'An error occurred.');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}