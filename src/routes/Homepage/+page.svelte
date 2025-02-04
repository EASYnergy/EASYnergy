<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'; // Import goto from SvelteKit
  
    let h1Text = 'GORDON COLLEGE EVENT MANAGEMENT SYSTEM';
    let h2Text = 'College of Computer Studies';
    let displayedH1 = '';
    let displayedH2 = '';
  
    /** 
     * Typewriter effect function
     * @param {string} text - The text to animate
     * @param {function(string): void} setter - Function to update displayed text
     * @param {number} [delay=100] - Delay in milliseconds
     */
    async function typeWriter(text, setter, delay = 100) {
      for (let i = 0; i < text.length; i++) {
        setter(text.slice(0, i + 1));
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  
    /**
     * Function to handle the full animation cycle
     */
    async function animateText() {
      await typeWriter(h1Text, value => (displayedH1 = value));
      await typeWriter(h2Text, value => (displayedH2 = value));
      await new Promise(resolve => setTimeout(resolve, 1000)); // Pause before erasing
  
      for (let i = h2Text.length; i >= 0; i--) {
        displayedH2 = h2Text.slice(0, i);
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      for (let i = h1Text.length; i >= 0; i--) {
        displayedH1 = h1Text.slice(0, i);
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
  
    async function startLoop() {
      while (true) {
        await animateText();
      }
    }
  
    onMount(() => {
      startLoop();
    });
  
    // Navigate to homepage
    function goToEventmain() {
      goto('/Eventmain'); // Replace '/homepage' with the route you want to navigate to
    }
  </script>
  
  <div class="relative h-screen w-full overflow-hidden">
    <!-- Hero Section -->
    <div class="h-screen bg-cover bg-center relative" style="background-image: url('/gcccs_cover_nr.jpg');">
      <div class="absolute inset-0 bg-black bg-opacity-20 flex flex-col items-center justify-center text-center text-white pt-72">
        <h1 class="text-5xl font-bold text-orange-400">{displayedH1}</h1>
        <h2 class="text-3xl font-semibold text-orange-400 mt-2">{displayedH2}</h2>
        <p class="mt-4 max-w-xl text-lg">
          The ultimate event management platform for GCCCS, designed to simplify organizing, tracking, and participating in events.
        </p>
        <button 
          class="mt-6 px-6 py-3 bg-orange-500 hover:bg-orange-600 rounded-lg font-bold text-white"
          on:click={goToEventmain}>
          Get Started
        </button>
      </div>
    </div>
  
    <!-- Scroll Down Indicator -->
    <div class="absolute bottom-5 left-1/2 transform -translate-x-1/2 animate-bounce">
      <span class="text-white text-xl">&#8595;</span>
    </div>
  </div>
  
  <!-- Additional Info Section -->
  <div class="h-[50vh] bg-[#3c0503] text-white flex flex-col items-center justify-center p-8">
    <h2 class="text-3xl font-semibold text-orange-400">About Our Platform</h2>
    <p class="mt-4 max-w-2xl text-center text-lg">
      Our platform offers seamless event management features tailored for students, faculty, and staff.
    </p>
  </div>
  