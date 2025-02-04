<script lang="ts">

    export let event = {
      name: "Sample Event Name",
      description: "This is a brief description of the event.",
      date: "2025-01-25",
      location: "Main Hall, Gordon College",
      speaker: "John Doe"
    };
  
    let feedback = [
      {
        question: "How was the event host?",
        rating: "",
        comment: ""
      },
      {
        question: "How was the event venue?",
        rating: "",
        comment: ""
      },
      {
        question: "How helpful were the materials provided?",
        rating: "",
        comment: ""
      },
      {
        question: "How would you rate the event's time management?",
        rating: "",
        comment: ""
      },
      {
        question: "Overall, how satisfied are you with the event?",
        rating: "",
        comment: ""
      }
    ];
  
    let showPrompt = false;

    const handleSubmit = () => {
      console.log("Feedback Submitted:", feedback);
      showPrompt = true;
    };

    const handlePromptClose = () => {
      showPrompt = false;
      history.back();
    };

    const goBack = () => {
        history.back();
    };
</script>

<!-- Event Header -->
<div class="flex items-start p-3 mb-4 bg-gradient-to-r from-[#400000] to-white">
    <button 
        on:click={goBack} 
        aria-label="Back to Events"
        class="mr-4 mt-2 mb-1 text-orange-400 hover:text-gray-800 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
    </button>
    <div>
        <h1 class="text-2xl mt-2 font-bold text-white">Post Evaluation for Event</h1>
    </div>
</div>
  
<div class="flex items-center justify-start px-4">
    <div class="bg-white w-full max-w-full p-6 rounded-lg">
        <!-- Event Details Section -->
        <div class="mb-6">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">{event.name}</h1>
            <div class="flex-grow text-gray-700 space-y-2">
                <p>{event.description}</p>
                <p><strong>Date:</strong> {event.date}</p>
                <p><strong>Location:</strong> {event.location}</p>
                <p><strong>Speaker:</strong> {event.speaker}</p>
            </div>
        </div>
  
        <!-- Feedback Questions Section with 2-column Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 pt-3 gap-8">
            {#each feedback as question, index}
                <div class="space-y-4">
                    <!-- Question Title -->
                    <label
                        for={`rating-${index}`}
                        class="block text-gray-700 font-medium text-lg"
                    >
                        {question.question}
                    </label>
  
                    <!-- Rating Scale (1-5) -->
                    <div class="flex gap-2">
                        {#each [1, 2, 3, 4, 5] as rating}
                            <label class="flex items-center">
                                <input
                                    type="radio"
                                    name={`rating-${index}`}
                                    value={rating}
                                    bind:group={question.rating}
                                    class="mr-2"
                                />
                                {rating}
                            </label>
                        {/each}
                    </div>
                    <p class="text-sm text-gray-600 mt-1 font-sans">1 is the lowest rating</p>
                    <!-- Comment/Feedback Input -->
                </div>
            {/each}
        </div>
   <!-- Submit Button -->
   <div class="text-right mt-6">
    <button
        type="button"
        on:click={handleSubmit}
        class="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-2 rounded-md shadow focus:outline-none focus:ring-2 focus:ring-orange-400"
    >
        Submit Feedback
    </button>
</div>
    </div>
</div>
  
<!-- Prompt Message -->
{#if showPrompt}
<div
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50"
>
    <div class="bg-white w-full max-w-md p-6 rounded-lg shadow-lg text-center space-y-4">
        <h2 class="text-xl font-bold text-gray-800">Thank you for your feedback!</h2>
        <p class="text-gray-600">Your feedback has been successfully submitted.</p>
        <button
            on:click={handlePromptClose}
            class="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-2 rounded-md shadow focus:outline-none focus:ring-2 focus:ring-orange-400"
        >
            OK
        </button>
    </div>
</div>
{/if}