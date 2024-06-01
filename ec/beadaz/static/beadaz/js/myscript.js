const body = document.querySelector("body"),
      nav = document.querySelector("nav"),
      modeToggle = document.querySelector(".dark-light"),
      searchToggle = document.querySelector(".searchToggle"),
      sidebarOpen = document.querySelector(".sidebarOpen"),
      siderbarClose = document.querySelector(".siderbarClose");
      let getMode = localStorage.getItem("mode");
          if(getMode && getMode === "dark-mode"){
            body.classList.add("dark");
          }
// js code to toggle dark and light mode
      modeToggle.addEventListener("click" , () =>{
        modeToggle.classList.toggle("active");
        body.classList.toggle("dark");
        // js code to keep user selected mode even page refresh or file reopen
        if(!body.classList.contains("dark")){
            localStorage.setItem("mode" , "light-mode");
        }else{
            localStorage.setItem("mode" , "dark-mode");
        }
      });
// js code to toggle search box
        searchToggle.addEventListener("click" , () =>{
        searchToggle.classList.toggle("active");
      });
 
      
//   js code to toggle sidebar
sidebarOpen.addEventListener("click" , () =>{
    nav.classList.add("active");
});
body.addEventListener("click" , e =>{
    let clickedElm = e.target;
    if(!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("menu")){
        nav.classList.remove("active");
    }
});


$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url: "/pluscart",
        data:{
            prod_id: id
        },
        success:function(data){
            console.log("data = ", data);
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
        }
    })
})


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

// Product details js

// Get all similar product cards
const similarProductCards = document.querySelectorAll('.similar-product-card');

// Loop through each similar product card
similarProductCards.forEach((card) => {
  // Get the add to bag button for the current card
  const addToBagButton = card.querySelector('.similar-product-button');

  // Add a click event listener to the add to bag button
  addToBagButton.addEventListener('click', () => {
    // Add a class to the card to highlight it
    card.classList.add('selected');

    // Remove the class from all other cards
    similarProductCards.forEach((otherCard) => {
      if (otherCard !== card) {
        otherCard.classList.remove('selected');
      }
    });
  });
});
function addToCart() {
    var message = document.getElementById("cartMessage");
    message.textContent = "Added to cart!";
}

const button = document.querySelector('.soapply-button');

button.addEventListener('click', () => {
  // Redirect to the Soapply shop page
  window.location.href = 'https://www.soapply.com/shop';
});

// Testimonials
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    grabCursor: true,
    loop: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

// add to cart 
// document.addEventListener('DOMContentLoaded', function() {
//     var addToCartBtn = document.getElementById('addToCartBtn');
//     var addToCartMessage = document.getElementById('addToCartMessage');
    
//     addToCartBtn.addEventListener('click', function(event) {
//         event.preventDefault(); // Prevent the default form submission behavior
        
//         // Display the "Added to Cart" message
//         addToCartMessage.style.display = 'block';
        
//         // Hide the message after 2 seconds
//         setTimeout(function() {
//             addToCartMessage.style.display = 'none';
//         }, 2000);
//     });
// });