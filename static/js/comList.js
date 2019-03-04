/**
 * Created by в23 on 03.03.2019.
 */

buttons = document.getElementsByClassName('btn-delete')

for (var key in buttons) {

    if (buttons[key].tagName == "DIV") {
        buttons[key].addEventListener('click', deleteComment)
    }
}

function deleteComment(event) {
    btn = event.target;
    parent = btn.parentNode
    idComment = btn.parentNode.attributes['data-id-comment'].value;


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == 'OK') {
                //удаление в БД прошло успешно
                elemForDelete = document.getElementById('comment' + idComment)
                listCom = elemForDelete.parentNode
                listCom.removeChild(elemForDelete)
            }
        }
    }
    xhttp.open('POST', '/delete_comment/', true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.send('idComment=' + idComment);

}