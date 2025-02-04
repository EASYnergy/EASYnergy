<script lang="ts">
  import Header from '../Header/+page.svelte'; // Import Header component

  // Define the structure of a report event
  interface ReportEvent {
    event_id: number;
    event_name: string;
    location: string;
    event_date: string; // Use `Date` if needed
    status: string;
    id: number;
  }

  // Define variables
  let reportData: ReportEvent[] = [];
  let totalEvents = 0;
  let scheduledEvents = 0;
  let completedEvents = 0;

  // Fetch Report Data from Backend
  async function fetchReportData() {
    try {
      const response = await fetch('http://localhost:5000/api/events');
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();

     // Update counters
     totalEvents = data.total_events || 0;
      scheduledEvents = data.scheduled_events || 0;
      completedEvents = data.completed_events || 0;

      // Update table data
      reportData = data.events || [];
    } catch (error) {
      console.error('Error fetching report data:', error);
    }
  }

  // Fetch data on component mount
  fetchReportData();

  // Function to generate a report for a specific event
  function generateReport(eventId: number) {
    alert(`Generating report for event ID: ${eventId}`);
    // Add logic to generate/download a report as needed
  }
</script>

<Header /> <!-- Render the Header component -->

<div class="min-h-screen bg-gray-100 p-6">
  <!-- Report Title -->
  <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-800">Overall Report</h1>
      <p class="text-gray-600">Overview of the Events of Students and Faculties</p>
  </div>

  <!-- Summary Section -->
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
      <div class="p-4 bg-white shadow rounded-lg">
          <h2 class="text-lg font-semibold text-gray-700">Total Number of Events</h2>
          <p class="mt-2 text-2xl font-bold text-blue-500">{totalEvents}</p>
      </div>
      <div class="p-4 bg-white shadow rounded-lg">
          <h2 class="text-lg font-semibold text-gray-700">Upcoming Events</h2>
          <p class="mt-2 text-2xl font-bold text-green-500">{scheduledEvents}</p>
      </div>
      <div class="p-4 bg-white shadow rounded-lg">
          <h2 class="text-lg font-semibold text-gray-700">Completed Events</h2>
          <p class="mt-2 text-2xl font-bold text-red-500">{completedEvents}</p>
      </div>
  </div>

  <!-- Data Table -->
  <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full border-collapse">
          <thead class="bg-blue-500">
              <tr>
                  <th class="py-3 px-6 text-left text-white font-semibold">Event</th>
                  <th class="py-3 px-6 text-left text-white font-semibold">Type</th>
                  <th class="py-3 px-6 text-left text-white font-semibold">Location</th>
                  <th class="py-3 px-6 text-left text-white font-semibold">Event Date</th>
                  <th class="py-3 px-6 text-left text-white font-semibold">Status</th>
                  <th class="py-3 px-6 text-left text-white font-semibold">Action</th>
              </tr>
          </thead>
          <tbody>
            {#each reportData as event (event.id)}
            <tr class="even:bg-gray-100">
                <td class="py-3 px-6">{event.event_name}</td>
                <td class="py-3 px-6">{event.location}</td>
                <td class="py-3 px-6">{event.event_date}</td>
                <td 
                    class="py-3 px-6 font-bold" 
                    class:text-green-500={event.status === "Scheduled"}
                    class:text-red-500={event.status === "Completed"}>
                    {event.status}
                </td>
                <td class="py-3 px-6">
                    <button 
                        class="bg-orange-500 text-white py-1 px-4 rounded-md hover:bg-orange-600 transition-all"
                        on:click={() => generateReport(event.id)}>
                        Generate Report
                    </button>
                </td>
            </tr>
        {/each}
        
          </tbody>
      </table>
  </div>
</div>

<style>
  /* Add any global styles if necessary */
</style>
