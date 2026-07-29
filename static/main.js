// ================= PROFILE DROPDOWN =================

function toggleProfileMenu(){

    const menu = document.getElementById("profileMenu");

    if(menu){

        if(menu.style.display === "block"){

            menu.style.display = "none";

        }else{

            menu.style.display = "block";

        }

    }

}



// Funga menu ukibonyeza sehemu nyingine

document.addEventListener("click", function(event){


    const profile = document.querySelector(".profile-container");

    const menu = document.getElementById("profileMenu");


    if(profile && menu){


        if(!profile.contains(event.target)){


            menu.style.display = "none";


        }


    }


});




// ================= SIDEBAR ACTIVE =================

const links = document.querySelectorAll(".sidebar ul li a");


links.forEach(link => {


    link.addEventListener("click", function(){


        links.forEach(item => {

            item.classList.remove("active");

        });



        this.classList.add("active");


    });


});