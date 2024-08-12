
const loader = document.getElementById('preloader');
const login = document.getElementById('open-login')
const modal = document.getElementById('login-modal');

/*load do site*/
window.addEventListener('load', function(){
    loader.style.display = 'none';
});

/*header*/
document.addEventListener('DOMContentLoaded', function() {
    if(isHomePage == true){
        const header = document.querySelector('header');
        window.addEventListener('scroll', function(){
            if (window.scrollY > 100 && header.classList.contains('header_home')){
                header.classList.remove('header_home');
                header.classList.add('header_scrolled');
                document.getElementById('logo_pink').style.width = '200px'
                document.getElementById('perfil').style.width = '50px'
                document.getElementById('perfil').style.height = '50px'
                document.getElementById('img-header').style.width = '50px'
                document.getElementById('img-header').style.height = '50px'
            } else if (window.scrollY == 0 && header.classList.contains('header_scrolled')){
                header.classList.add('header_home');
                header.classList.remove('header_scrolled');
                document.getElementById('logo_pink').style.width = '250px'
                document.getElementById('perfil').style.width = '60px'
                document.getElementById('perfil').style.height = '60px'
                document.getElementById('img-header').style.width = '60px'
                document.getElementById('img-header').style.height = '60px'
            }

            /*responsividade do header quando a pagina é menor que 1400px*/
            if (window.innerWidth <= 1400 && header.classList.contains('header_home')){
                header.classList.remove('header_home');
                header.classList.add('header_scrolled');
                document.getElementById('logo_pink').style.width = '200px'
                document.getElementById('perfil').style.width = '50px'
                document.getElementById('perfil').style.height = '50px'
            } else if (window.innerWidth <= 1400 && header.classList.contains('header_scrolled')){
                header.classList.add('header_home');
                header.classList.remove('header_scrolled');
                this.document.getElementById('logo_pink').style.width = '200px'
            }
        });
    } else {
        document.getElementById('logo_pink').style.width = '200px'
        document.getElementById('perfil').style.width = '50px'
        document.getElementById('perfil').style.height = '50px'
        document.getElementById('img-header').style.width = '50px'
        document.getElementById('img-header').style.height = '50px'
    }
});

/*modal login*/
login.addEventListener('click', function(){
    if (modal.classList.contains('closed-modal')){
        modal.classList.remove('closed-modal');
        modal.classList.add('open-modal');
    }else if (modal.classList.contains('open-modal')){
        modal.classList.remove('open-modal');
        modal.classList.add('closed-modal');
    }
});