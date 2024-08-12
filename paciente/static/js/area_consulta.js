// const btnExcluir = document.getElementById('icon-delete');
// const btnNao = document.getElementById('Nao');
// const modalExcluir = document.getElementById('posicao-confirm');

// /*botão de edit*/
// btnExcluir.addEventListener('click', function(){
//     if (modalExcluir.classList.contains('confirm-closed')){
//         modalExcluir.classList.remove('confirm-closed');
//         modalExcluir.classList.add('confirm-open');
//     }
// });

// btnNao.addEventListener('click', function(){
//     modalExcluir.classList.remove('confirm-open');
//     modalExcluir.classList.add('confirm-closed');
// });

const btnRemake = document.getElementById('icon-reload');
const btnCancelar = document.getElementById('Nao-remake');
const modalRemake = document.getElementById('posicao-remake');

/*botão de edit*/

btnRemake.addEventListener('click', function(){
    if (modalRemake.classList.contains('remake-closed')){
        modalRemake.classList.remove('remake-closed');
        modalRemake.classList.add('remake-open');
    }
});

btnCancelar.addEventListener('click', function(){
    modalRemake.classList.remove('remake-open');
    modalRemake.classList.add('remake-closed');
});

