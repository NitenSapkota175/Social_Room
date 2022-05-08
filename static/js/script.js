// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

//for delete pop up

var mymodel = document.getElementById("mytoggle");
var myBtn = document.getElementById("btn");
var span = document.getElementsByClassName("close")[0];
var pop = document.getElementById("popUp");


myBtn.onclick = function() {
   pop.style.display = "block";
   mymodel.style.display = "none";
}

span.onclick = function() {
  mymodel.style.display = "block";
  pop.style.display = "none";
}

// delete pop up ends here

// for opening the comment section
document.getElementById("openComment").onclick = function() {
  myFunction("commentOpen");
}

function myFunction(p1)
{
  console.log(p1)
  var open = document.getElementById(p1);
  if(open.style.display === 'none')
  {
    open.style.display = "block";
  }
  else
  {
    open.style.display = "none";
  }
}


//for closing the comment section
document.getElementById('delete').onclick = function () {
  myDeleteFunction("commentOpen");
}

function myDeleteFunction(p2)
{
  console.log(p2);
  var close = document.getElementById(p2);

  if(close.style.display === "block")
  {
    close.style.display = 'none';
  }
  else
  {
    close.style.display = " block";
  }
}


//for the like and dislike
let likebtn = document.querySelector('#likePic');
let dislikebtn = document.querySelector('#dislikePic');
let input1 = document.querySelector('#number1');
let input2 = document.querySelector('#number2');

likebtn.addEventListener('click', ()=>{
  input1.value = parseInt(input1.value) + 1;
  input1.style.color = "white";
});

dislikebtn.addEventListener('click', ()=>{
   input2.value = parseInt(input2.value) + 1;
   input2.style.color = "white";
});




// taking inputtext from input and appending it to the li and appending li to the ul which is already inside the list-comment

document.getElementById('addItem').addEventListener('click', () => {
  var input = document.getElementById('inputText');
  var inputData = input.value.split('\n');
  var listContainer = document.getElementById('list');
  var listData = document.createElement('ul');
  listContainer.appendChild(listData);

  var numberOfInput = inputData.length;
  var listItem;

  //if input field is empty it will alret you 
  if(input.value === '')
  {
    alert('Write Something....');
  }
  else if(input.value === ' ')
  {
    alert('Write Something....');
  }
  //and if input does contains some values then it will added in the below section
  else{
    for(var i = 0; i < numberOfInput; i++)
    {
    listItem = document.createElement('li');
    listItem.appendChild(document.createTextNode(input.value));
    listItem.style.listStyle = "none";
    listData.appendChild(listItem);
    }
    document.getElementById('inputText').value = ' ';
  }
});

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}


// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;
