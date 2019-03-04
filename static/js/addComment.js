//модальное окно
var modal = document.getElementById('myModal');
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function checkInput(idElement) {
    if (document.getElementById(idElement).value == "") {
        document.getElementById(idElement).classList.add('empty')
        document.getElementById(idElement).placeholder = 'Указажите значение'
        return 1
    }
    document.getElementById(idElement).classList.remove('empty')
    return 0
}


function checkPhoneOrEmail(idElement, reg) {
    var field = document.getElementById(idElement).value;
    if (!reg.test(field)) {
        document.getElementById(idElement).classList.add('empty')
        document.getElementById(idElement).placeholder = 'Введите корректные данные'
        return 1
    }
    document.getElementById(idElement).classList.remove('empty')
    return 0
}

var saveButton = document.getElementById('saveComment')
saveButton.addEventListener('click', saveCommentOnServer)


function saveCommentOnServer(event) {
    event.preventDefault();

    var errors = 0

    //проверка ФИ и коммент
    errors += checkInput('surname')
    errors += checkInput('first_name')
    errors += checkInput('comment')

    //проверка phone
    var reg = /^[+\d][\d\(\)\ -]{4,14}\d$/;
    errors += checkPhoneOrEmail('phone', reg)

    //проверка email
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    errors += checkPhoneOrEmail('email', reg)

    if (errors > 0) {
        return false
    }

    var form_data = ''
    var form = new FormData(document.getElementById('add_comment'));

    for (var key of form.keys()) {
        form_data += key + '=' + form.get(key) + '&'
        console.log(key)
        document.getElementById(key).value = ''
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "OK") {
                var modal = document.getElementById('myModal');
                modal.style.display = "block"

            }
        }
    }
    xhttp.open('POST', '/save/', true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.send(form_data);
}


var region = document.getElementById('region');
region.addEventListener('change', getCities);

function getCities() {
    var idRegion = region.options[region.selectedIndex].value;
    var rid = 'region_id=' + idRegion;
    city = document.getElementById('city');

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            city.innerHTML = '';
            city.innerHTML += this.responseText;
        }
    }
    xhttp.open('POST', '/get_city/', true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.send(rid);
}