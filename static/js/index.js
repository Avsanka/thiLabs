$(document).ready(() =>
    {
        $.ajax({
                type: 'GET',
                url: '/getFilms',
                dataType: 'json',
                success: function(films) {
                    const $tbody = $('#filmsTable');
                    $tbody.empty();
                    for (let i = 0; i < films.length; i++) {
                        const film = films[i];
                        const title = film.title;
                        const year = film.year;
                        const rating = film.rating;
                        const director = film.director;
                        const row = `
                            <tr style="cursor: pointer;" data-id="${film.id}"'>
                                <td>${title}</td>
                                <td>${year}</td>
                                <td>${rating}</td>
                                <td>${director}</td>
                            </tr>
                        `;
                        $tbody.append(row);
                    }
                    $('#filmsTable tr').click(function() {
                        const filmId = $(this).data('id');
                        window.location.href = `/filmInfo?id=${filmId}`;
                    });
                },
            });

    });

