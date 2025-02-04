<script lang="ts">
  import { goto } from '$app/navigation';

  let email = '';
  let password = '';
  let username = '';
  let role = '';
  let isSignup = false;
  let currentImageIndex = 0;

  // Function to handle login
  async function handleLogin() {
  if (username.trim() !== '' && password.trim() !== '') {
    try {
      const response = await fetch('http://localhost:5000/api/user/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      console.log('Response:', response);

      if (response.ok) {
        const data = await response.json();
        console.log('Data:', data);
        alert('Login successful!');
        goto('/Homepage'); // Navigate to Eventmain page
      } else {
        const errorData = await response.text();
        console.error('Error Response:', errorData);
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred. Please try again.');
    }
  } else {
    alert('Please fill in both username and password.');
  }
}



  // Function to handle signup
  async function handleSignup() {
  if (username.trim() !== '' && email.trim() !== '' && password.trim() !== '' && role.trim() !== '') {
    try {
      console.log('Sending signup data:', { username, email, password, role });

      const response = await fetch('http://localhost:5000/api/user/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, role }),
      });

      // Check if the response is OK
      if (response.ok) {
        const data = await response.json();
        console.log('Signup response:', data);
        alert('Signup successful!');
        isSignup = false; // Switch back to login form
      } else {
        const errorData = await response.text();
        console.error('Signup failed:', errorData);
        alert('Signup failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during signup:', error);
      alert('An error occurred. Please try again.');
    }
  } else {
    alert('Please fill in all fields.');
  }
}

let images = [
    "/ccs_logo.png",
    "/gc_new_logo_2018.png",
    "/EASYnergy.png",
  ];

// Cycle through logos
function cycleLogo() {
    currentImageIndex = (currentImageIndex + 1) % images.length;
  }

  // Start logo cycling
  setInterval(cycleLogo, 5000);
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');

  h1, h2, form {
    font-family: 'Raleway', sans-serif;
  }

  .logo-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
    backdrop-filter: blur(5px);
  }

  .logo {
    max-height: 4rem;
    max-width: 200px;
    object-fit: contain;
    position: absolute;
    opacity: 0;
    transition: opacity 2s ease-in-out;
  }

  .logo.active {
    opacity: 3;
  }

  
</style>

<div class="content-wrapper">
  <div class="logo-container">
    {#each images as image, index}
    <img
      src={image}
      alt={`Logo ${index}`}
      class="logo {index === currentImageIndex ? 'active' : ''}"
    />
  {/each} 
  </div>

  <div class="fixed w-full h-full pb-0 grid grid-cols-3" style="background-color: #400000; top: 0; left: 0;">
    <!-- Left Column -->
    <div class="flex items-center justify-start bg-transparent opacity-70">
      <img
        src="/right_half_log.png"
        alt="Right Half Logo"
        class="h-auto w-full max-w-[64%] object-contain"/>
    </div>

    <!-- Center Column -->
    <div class="flex flex-col items-center justify-center bg-transparent text-white px-4 py-8">
      <div class="mb-8 text-center">
        <h1 class="text-2xl md:text-3xl font-bold text-orange-400">GORDON COLLEGE</h1>
        <h2 class="text-xl md:text-2xl font-semibold text-orange-400 mt-2">
          COLLEGE OF COMPUTER STUDIES
        </h2>
      </div>

      <div class="w-full max-w-md p-6 bg-white bg-opacity-20 backdrop-blur-md rounded-lg shadow-lg">
        {#if isSignup}
          <h2 class="text-xl md:text-2xl font-bold text-white text-center mb-6">Signup</h2>
          <form on:submit|preventDefault={handleSignup}>
            <div class="mb-4">
              <label for="username" class="block text-sm font-medium text-white">Username</label>
              <input
                type="text"
                id="username"
                bind:value={username}
                placeholder="Enter your username"
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"/>
            </div>
            <div class="mb-4">
              <label for="email" class="block text-sm font-medium text-white">Email</label>
              <input
                type="email"
                id="email"
                bind:value={email}
                placeholder="Enter your email"
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"/>
            </div>
            <div class="mb-4">
              <label for="password" class="block text-sm font-medium text-white">Password</label>
              <input
                type="password"
                id="password"
                bind:value={password}
                placeholder="Enter your password"
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"/>
            </div>
            <div class="mb-6">
              <label for="role" class="block text-sm font-medium text-white">Role</label>
              <select
                id="role"
                bind:value={role}
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none">
                <option value="">Select your role</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <button
              type="submit"
              class="w-full py-2 px-4 bg-orange-500 text-white font-bold rounded-lg hover:bg-orange-600 focus:outline-none">
              Signup
            </button>
          </form>
          <p class="text-sm text-center text-white mt-4">
            Already have an account?
            <button
              type="button"
              class="font-semibold text-orange-400 hover:underline"
              on:click={() => (isSignup = false)}>
              Login here
            </button>
          </p>
        {:else}
          <h2 class="text-xl md:text-2xl font-bold text-white text-center mb-6">Login</h2>
          <form on:submit|preventDefault={handleLogin}>
            <div class="mb-4">
              <label for="username" class="block text-sm font-medium text-white">Username</label>
              <input
                type="text"
                id="username"
                bind:value={username}
                placeholder="Enter your username"
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"/>
            </div>
            <div class="mb-6">
              <label for="password" class="block text-sm font-medium text-white">Password</label>
              <input
                type="password"
                id="password"
                bind:value={password}
                placeholder="Enter your password"
                class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-white rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"/>
            </div>
            <button
              type="submit"
              class="w-full py-2 px-4 bg-orange-500 text-white font-bold rounded-lg hover:bg-orange-600 focus:outline-none">
              Login
            </button>
          </form>
          <p class="text-sm text-center text-white mt-4">
            Don't have an account?
            <button
              type="button"
              class="font-semibold text-orange-400 hover:underline"
              on:click={() => (isSignup = true)}>
              Signup here
            </button>
          </p>
        {/if}
      </div>

      {#if !isSignup}
        <p class="text-sm text-orange-400 text-center mt-4 px-2">
          Stay connected and engaged with events that matter to you! Discover, track, and participate in events seamlessly through our platform.
        </p>
      {/if}
    </div>

    <!-- Right Column -->
    <div class="flex items-center justify-end bg-transparent opacity-70">
      <img
        src="/left_half_logo.png"
        alt="Left Half Logo"
        class="h-auto w-full max-w-[65%] object-contain"/>
    </div>
  </div>
</div>