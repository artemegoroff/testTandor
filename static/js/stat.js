/**
 * Created by в23 on 03.03.2019.
 */

var rows = document.getElementsByClassName('clickable-row')
for (var key in rows) {
    if (rows[key].tagName == 'TR') {
        rows[key].addEventListener('click', cityStat);
    }
}
function cityStat(event) {
    var url = event.target.parentNode.dataset['href']
    if (url.length > 0) {
        window.location = url
    }
}