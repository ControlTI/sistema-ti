function selecionarFilial(botao, filial){

    document.getElementById(
        'filial'
    ).value = filial

    let botoes =
        document.querySelectorAll('.filial-btn')

    botoes.forEach(btn => {
        btn.classList.remove('filial-active')
    })

    botao.classList.add('filial-active')

}

function abrirSenha(){

    document.getElementById(
        'modalSenha'
    ).style.display = 'flex'

}

function abrirPrimeiroAcesso(){

    document.getElementById(
        'modalPrimeiroAcesso'
    ).style.display = 'flex'

}

window.onclick = function(event){

    let modalSenha =
        document.getElementById('modalSenha')

    let modalPrimeiro =
        document.getElementById('modalPrimeiroAcesso')

    if(event.target == modalSenha){
        modalSenha.style.display = 'none'
    }

    if(event.target == modalPrimeiro){
        modalPrimeiro.style.display = 'none'
    }

}


function toggleMenu(id){

    let menu =
        document.getElementById(id)

    if(menu.style.display === 'block'){

        menu.style.display = 'none'

    }else{

        menu.style.display = 'block'

    }

}


