document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".header-image");

  let currentIndex = 0;

  function changeImage() {
    currentIndex = (currentIndex + 1) % images.length;
    header.style.backgroundImage = `url(${images[currentIndex]})`;
  }

  console.log(images);

  // Dastlabki rasm o'rnatilishi (agar kerak bo'lsa)
  header.style.backgroundImage = `url(${images[0]})`;

  // Har 3 soniyada rasmni o'zgartirish
  setInterval(changeImage, 3000);
});
