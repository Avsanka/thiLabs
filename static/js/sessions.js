$(document).ready(() =>
{
    const urlParams = new URLSearchParams(window.location.search);
    const allSessions = urlParams.get('allSessions');

    if (allSessions){ url = '/getSessions?allSessions=1'; $('#label').html('<h2>Все сеансы</h2');}
    else {url = '/getSessions';}
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(sessions) {
            if (sessions.length === 0) {
                $('#sessions').html('<p>Сеансов нет</p>');
                return;
            }
            let allCards = '';
            for (let i = 0; i < sessions.length; i++) {
                let s = sessions[i];
                let datetime = new Date(s.datetime);

                allCards = allCards + `
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <img src="${s.img}" class="card-img-top" style="max-height: 530px">
                            <div class="card-body">
                                <h5>${s.title} (${s.year})</h5>
                                <p>Зал: ${s.hall}<br>
                                   Дата: ${datetime.toLocaleDateString('ru-RU')}<br>
                                   Время: ${datetime.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}<br>
                                   Цена: ${s.price} ₽</p>
                                <button class="btn btn-primary" onclick="buyTicket(${s.id})">Купить</button>
                            </div>
                        </div>
                    </div>
                `;
            }

            $('#sessions').html(allCards);
        },
        error: function() {
            $('#sessions').html('<p style="color:red">Ошибка загрузки</p>');
        }
    });

});

function buyTicket(id)
{
    window.location.href = '/buyTicket?id=' + id;
}