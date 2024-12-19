<script lang="ts">
  import { goto } from '$app/navigation';

  let email = '';
  let password = '';
  let username = '';
  let role = '';
  let isSignup = false;

  // Function to handle login
  async function handleLogin() {
  if (email.trim() !== '' && password.trim() !== '') {
    try {
      const response = await fetch('http://localhost/EASYnergy/login.php', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      console.log('Response:', response);

      if (response.ok) {
        const data = await response.json();
        console.log('Data:', data);
        alert('Login successful!');
        goto('/Eventmain'); // Navigate to Eventmain page
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
    alert('Please fill in both email and password.');
  }
}


  // Function to handle signup
  async function handleSignup() {
  if (username.trim() !== '' && email.trim() !== '' && password.trim() !== '' && role.trim() !== '') {
    try {
      console.log('Sending signup data:', { username, email, password, role });

      const response = await fetch('http://localhost/EASYnergy/signup.php', {
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
</script>

<div class="fixed w-full h-full pb-0 grid grid-cols-3" style="background-color: #400000;">
  <!-- Left Column -->
  <div class="flex items-center justify-start bg-transparent mt-[-140px] opacity-70">
    <img src="/right_half_log.png" alt="Right Half Logo" class="h-[60%] w-auto" />
  </div>

  <!-- Center Column -->
  <div class="flex flex-col items-center justify-center bg-transparent text-white mt-[-100px]">
    <!-- Title -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-orange-400">GORDON COLLEGE</h1>
      <h2 class="text-2xl font-semibold text-orange-400 mt-2">COLLEGE OF COMPUTER STUDIES</h2>
    </div>

    <!-- Form -->
    <div class="w-96 p-6 bg-white bg-opacity-20 backdrop-blur-md rounded-lg shadow-lg">
      {#if isSignup}
        <!-- Signup Form -->
        <h2 class="text-2xl font-bold text-white text-center mb-6">Signup</h2>
        <form on:submit|preventDefault={handleSignup}>
          <div class="mb-4">
            <label for="username" class="block text-sm font-medium text-white">Username</label>
            <input
              type="text"
              id="username"
              bind:value={username}
              placeholder="Enter your username"
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-white">Email</label>
            <input
              type="email"
              id="email"
              bind:value={email}
              placeholder="Enter your email"
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div class="mb-4">
            <label for="password" class="block text-sm font-medium text-white">Password</label>
            <input
              type="password"
              id="password"
              bind:value={password}
              placeholder="Enter your password"
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div class="mb-6">
            <label for="role" class="block text-sm font-medium text-white">Role</label>
            <select
              id="role"
              bind:value={role}
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none">
              <option value="">Select your role</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <button
            type="submit"
            class="w-full py-2 px-4 bg-orange-500 text-white font-bold rounded-lg hover:bg-orange-600 focus:none focus:outline-none">
            Signup
          </button>
        </form>
        <p class="text-sm text-center text-white mt-4"> 
          <button type="button" class="font-semibold text-orange-400 hover:underline" on:click={() => (isSignup = false)}>Login here</button>
          Already have an account?
        </p>
      {:else}
        <!-- Login Form -->
        <h2 class="text-2xl font-bold text-white text-center mb-6">Login</h2>
        <form on:submit|preventDefault={handleLogin}>
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-white">Email</label>
            <input
              type="email"
              id="email"
              bind:value={email}
              placeholder="Enter your email"
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <div class="mb-6">
            <label for="password" class="block text-sm font-medium text-white">Password</label>
            <input
              type="password"
              id="password"
              bind:value={password}
              placeholder="Enter your password"
              class="mt-1 block w-full px-4 py-2 bg-transparent border-2 text-black rounded-lg focus:ring-2 focus:ring-orange-400 focus:outline-none"
            />
          </div>
          <button
            type="submit"
            class="w-full py-2 px-4 bg-orange-500 text-white font-bold rounded-lg hover:bg-orange-600 focus:none focus:outline-none">
            Login
          </button>
        </form>
        <p class="text-sm text-center text-white mt-4">
          Don't have an account? <button type="button" class="font-semibold text-orange-400 hover:underline" on:click={() => (isSignup = true)}>Signup here</button>
        </p>
      {/if}
    </div>

    {#if !isSignup}
      <h6 class="text-sm text-orange-400 text-center mt-3">The ultimate event management platform for GCCCS, designed to simplify the process of organizing, tracking, and participating in events. From academic seminars to student-led activities, we provide a seamless experience for all. Stay connected, informed, and engaged with events that matter to you!</h6>
    {/if}
  </div>

  <!-- Right Column -->
  <div class="flex items-center justify-end bg-transparent mt-[-150px] opacity-70">
    <img src="/left_half_logo.png" alt="Left Half Logo" class="h-[60%] w-auto" />
  </div>
</div>