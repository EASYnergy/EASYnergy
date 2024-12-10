<script>
    let email = '';
    let password = '';
</script>

<style>

h1{
        font-family: 'Times New Roman', Times, serif;   
  font-weight: 400;
  font-style: normal;
  font-size: 26px;
    }

    h2{
        font-family: 'Times New Roman', Times, serif;   
  font-weight: 400;
  font-style: normal;
  font-size: 28px;
    }

    h6{
        font-weight: lighter;
  font-style: normal;
  font-size: 14px;
    line-height: 1.2;
    }
    
    </style>

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
            <h2 class="text-2xl font-bold text-white text-center mb-6">Login</h2>
            <form>
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
                    class="w-full py-2 px-4 bg-orange-500 text-white font-bold rounded-lg hover:bg-orange-600 focus:none  focus:outline-none">
                    Login
                </button>
            </form>
        </div>
        <h6 class="font-bold text-white text-center mt-3">The ultimate event management platform for GCCCS, designed to simplify the process of organizing, tracking, and participating in events. From academic seminars to student-led activities, we provide a seamless experience for all. Stay connected, informed, and engaged with events that matter to you!

        </h6>
    </div>

    <!-- Right Column -->
    <div class="flex items-center justify-end bg-transparent mt-[-150px] opacity-70">
        <img src="/left_half_logo.png" alt="Left Half Logo" class="h-[60%] w-auto" />
    </div>
</div>