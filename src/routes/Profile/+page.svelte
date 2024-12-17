<script>

import Header from '../Header/+page.svelte'; // Import Header component

    let user = {
      profilePic: "https://via.placeholder.com/150",
      studentid: "202210044",
      fullname: "Aaron Clark Perez",
      role: "President",
      department: "BSIT",
      yearlevel: "3rd year",
  
    };
  </script>

<Header /> <!-- Render the Header component -->
  
  <div class="flex items-center justify-center min-h-screen bg-orange-100">
    <!-- Main Container -->
    <div class="flex flex-row items-center bg-orange-50 p-6 square-lg shadow-md max-w-4xl w-50s">
      <!-- Profile Picture -->
      <div class="flex-shrink-0 w-40 h-40 square-full overflow-hidden border-4 border-white shadow-lg">
        <img 
        src={user.profilePic} 
        alt="{user.fullname}'s profile picture" 
        class="w-full h-full object-cover"
      />
      </div>
  
      <!-- Info Section -->
      <div class="ml-8 text-left space-y-4"> <!-- Added consistent spacing -->
        <p class="text-xl text-gray-700"><strong>Student Number:</strong> {user.studentid}</p>
        <p class="text-xl text-gray-700"><strong>Full Name:</strong> {user.fullname}</p>   
        <p class="text-xl text-gray-700"><strong>Role:</strong> {user.role}</p>
        <p class="text-xl text-gray-700"><strong>Department:</strong> {user.department}</p>
        <p class="text-xl text-gray-700"><strong>Year Level:</strong> {user.yearlevel}</p>
      </div>
    </div>
  </div>
  
  <style>
    /* Global or additional styles */
  </style>
  
