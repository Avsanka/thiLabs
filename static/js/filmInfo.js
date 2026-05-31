$(document).ready(() =>
        {
            const urlParams = new URLSearchParams(window.location.search);
            const filmId = urlParams.get('id');

            $.ajax({
                type: 'GET',
                url: '/filmInfoById',
                data: { id: filmId },
                dataType: 'json',
                success: function(data) {
                    const film = data[0];
                    let html = `
                        <h1>${film.title} (${film.year})</h1>
                        <div style="display: flex;">
                            <div class="w-25">
                                <img src="${film.img}" class="w-100">
                            </div>
                            <div>
                                <div class="ms-5">
                                    <p><strong>Режиссёр:</strong> ${film.director}</p>
                                    <p><strong>Рейтинг:</strong> ${film.rating}</p>
                                    <p><strong>Длительность:</strong> ${film.duration} мин.</p>
                                    <p><strong>Жанр:</strong> ${film.genre}</p>
                                    <p><strong>Страна:</strong> ${film.country}</p>
                                    <p><strong>Описание:</strong> ${film.description || 'Нет описания'}</p>
                                </div>
                            </div>
                        </div>
                    `;
                    $('#filmInfo').html(html);
                },
            });
        });