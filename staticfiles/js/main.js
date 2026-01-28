menuDropDownList = document.getElementById('menu-drop-down').addEventListener('click', function () {
    this.nextElementSibling.classList.toggle('active')
    this.nextElementSibling.nextElementSibling.classList.toggle('active')
})

categoryDropDownList = document.getElementById('category-drop-down-list').addEventListener('click', function () {
    this.classList.toggle('active')
})