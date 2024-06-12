// Django project name: Huddle
// Django app name: Huddle_app
// Course: CS 4800 - SWE

document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    if (event.code === 'Escape') {
      closeAllModals();
    }
  });

  // Add a click event to the "Cancel" button
  const cancelButton = document.getElementById('cancelButton');
  cancelButton.addEventListener('click', () => {
    // Find the closest modal and close it
    const modal = cancelButton.closest('.modal');
    closeModal(modal);

    // Reset input values to their placeholders
    document.getElementById('huddleName').value = '';
    document.getElementById('members').value = '';

  });  

});

function createHuddle() {
  // Obtain values from user input from id="createHuddleForm"
  var huddleName = document.getElementById('huddleName').value;
  var members = document.getElementById('members').value;
  // Huddle group card html template
  var huddleTemplate = `
  <div class="column is-one-third">
    <div class="card">
      <div class="card-image">
        <figure class="image">
          <img src="/static/huddle_default.png" alt="default huddle photo">
        </figure>
      </div>
      <div class="card-content card-content-size">
        <div class="media">
          <div class="media-content">
            <p class="title is-4">
              <a href="javascript:void(0);" class="toggle-content">${huddleName}</a>
            </p>
          </div>
        </div>
        <div class="huddle-content" style="display: none;">
        <p class="huddle-members">Members: ${members}</p>
        </div>
      </div>
    </div>
  </div>
  `;

  // Insert HTML to id="cardContainer"
  const cardContainer = document.getElementById('cardContainer');
  cardContainer.insertAdjacentHTML('beforeend', huddleTemplate);

  // Reset input fields
  document.getElementById('huddleName').value = '';
  document.getElementById('members').value = '';


  // Add a click event listener to the title link in the newly created card
  var titleLinks = document.querySelectorAll(".toggle-content");
  titleLinks[titleLinks.length - 1].addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default link behavior
    var huddleContent = this.closest(".card-content").querySelector(".huddle-content");

    // Toggle the visibility of the huddle content
    if (huddleContent) {
      if (huddleContent.style.display === "none") {
        huddleContent.style.display = "block";
      } else {
        huddleContent.style.display = "none";
      }
    }
  });
}


function addMember(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Obtain values from user input from id="addMemberForm"
  var memberName = document.getElementById('memberName').value;
  var memberEmail = document.getElementById('memberEmail').value;

  // Create a new member card HTML template
  var memberTemplate = `
    <div class="column is-one-third">
      <div class="card rounded-edges">
        <div class="card-content">
          <p class="name">${memberName}</p>
        </div>
        <footer class="card-footer" style="justify-content: center;">
          <div class="py-3 px-3">
            <a class="pl-2" href="mailto:${memberEmail}" target="_blank">
              <i class="fas fa-2x fa-envelope"></i>
            </a>
          </div>
        </footer>
      </div>
    </div>
  `;

  // Insert the new member card HTML into the members-container
  const membersContainer = document.getElementById('columns-container');
  membersContainer.insertAdjacentHTML('beforeend', memberTemplate);
    // Reset input fields--
    document.getElementById('memberName').value = '';
    document.getElementById('memberEmail').value = '';
   
}


document.addEventListener("DOMContentLoaded", function() {
  var groupNavigation = document.getElementById("groupNavigation");
  var body = document.body;
  var offset = groupNavigation.offsetTop;

  function handleScroll() {
      if (window.scrollY >= offset) {
          groupNavigation.classList.add("is-fixed-top");
          body.classList.add("fixed-nav-padding");
      } else {
          groupNavigation.classList.remove("is-fixed-top");
          body.classList.remove("fixed-nav-padding");
      }
  }

  window.addEventListener("scroll", handleScroll);
});

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    selectable: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    dateClick: function(info) {
      alert('clicked ' + info.dateStr);
    },
  });
 calendar.render();
});



function toggleTaskCard(header) {
  const content = header.nextElementSibling;
  content.style.display = (content.style.display === 'none' || content.style.display === '') ? 'block' : 'none';
}

function deleteTask(footer) {
  const card = footer.parentElement.parentElement;
  card.remove(); // Remove the entire card element
}


document.addEventListener('DOMContentLoaded', () => {

  // Add a click event on the "Task + button"
  const addTaskButton = document.getElementById('addTaskButton');
  addTaskButton.addEventListener('click', () => {
      const modal = addTaskButton.dataset.target;
      const $target = document.getElementById(modal);
      openModal($target);
  });
});

function addTask(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Obtain values from user input from id="addTaskForm"
  var taskName = document.getElementById('taskName').value;
  var taskDescription = document.getElementById('taskDescription').value;
  var assignedMembers = document.getElementById('assignedMembers').value;
  var dueDate = document.getElementById('dueDate').value;

  // Task card HTML template
  var taskTemplate = `
      <div class="card">
          <header class="card-header" onclick="toggleTaskCard(this)">
              <p class="card-header-title">
                  ${taskName}
              </p>
              <button class="card-header-icon" aria-label="more options">
                  <span class="icon">
                      <i class="fas fa-angle-down" aria-hidden="true"></i>
                  </span>
              </button>
          </header>
          <div class="card-content">
              <div class="content">
                  Description: ${taskDescription}
                  <br>
                  Assigned Members: ${assignedMembers}
              </div>
          </div>
          <footer class="card-footer">
              <p class="card-footer-item">Due Date: ${dueDate}</p>
              <a href="#" class="card-footer-item" onclick="deleteTask(this)">Delete</a>
          </footer>
      </div>
  `;

  // Insert the new task card HTML into the tasks container
  const tasksContainer = document.getElementById('tasks-container');
  tasksContainer.insertAdjacentHTML('beforeend', taskTemplate);

  // Reset input fields
  document.getElementById('taskName').value = '';
  document.getElementById('taskDescription').value = '';
  document.getElementById('assignedMembers').value = '';
  document.getElementById('dueDate').value = '';
}


