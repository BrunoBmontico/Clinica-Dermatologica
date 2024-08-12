const btnEditar = document.getElementById('editar');
const btnCancel = document.getElementById('cancel');
const modalEdit = document.getElementById('container-modalEdit');

/*botão de edit*/
btnEditar.addEventListener('click', function(){
    if (modalEdit.classList.contains('edit-closed')){
        modalEdit.classList.remove('edit-closed');
        modalEdit.classList.add('edit-open');
    }
});

btnCancel.addEventListener('click', function(){
    modalEdit.classList.remove('edit-open');
    modalEdit.classList.add('edit-closed');
});