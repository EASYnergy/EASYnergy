<script>
        import Header from '../Header/+page.svelte'; // Import Header component
    let reportData = [
      { id: 202210078, name: "Aaron", role: "President", status: "Active", lastUpdated: "2024-12-10" },
      { id: 202210168, name: "Eunice", role: "Secretary", status: "Inactive", lastUpdated: "2024-11-15" },
      { id: 202210606, name: "Yzer", role: "Vice President", status: "Active", lastUpdated: "2024-12-01" },
    ];
  </script>

<Header /> <!-- Render the Header component -->
  
  <div class="min-h-screen bg-gray-100 p-6">
    <!-- Report Title -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-800">Overall Report</h1>
      <p class="text-gray-600">Overview of student activities and updates</p>
    </div>
  
    <!-- Summary Section -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
      <div class="p-4 bg-white shadow rounded-lg">
        <h2 class="text-lg font-semibold text-gray-700">Total Students</h2>
        <p class="mt-2 text-2xl font-bold text-blue-500">{reportData.length}</p>
      </div>
      <div class="p-4 bg-white shadow rounded-lg">
        <h2 class="text-lg font-semibold text-gray-700">Active Students</h2>
        <p class="mt-2 text-2xl font-bold text-green-500">{reportData.filter(e => e.status === "Active").length}</p>
      </div>
      <div class="p-4 bg-white shadow rounded-lg">
        <h2 class="text-lg font-semibold text-gray-700">Inactive Students</h2>
        <p class="mt-2 text-2xl font-bold text-red-500">{reportData.filter(e => e.status === "Inactive").length}</p>
      </div>
    </div>
  
    <!-- Data Table -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full border-collapse">
        <thead class="bg-blue-500">
          <tr>
            <th class="py-3 px-6 text-left text-white font-semibold">ID</th>
            <th class="py-3 px-6 text-left text-white font-semibold">Name</th>
            <th class="py-3 px-6 text-left text-white font-semibold">Role</th>
            <th class="py-3 px-6 text-left text-white font-semibold">Status</th>
            <th class="py-3 px-6 text-left text-white font-semibold">Last Updated</th>
          </tr>
        </thead>
        <tbody>
          {#each reportData as employee (employee.id)}
            <tr class="even:bg-gray-100">
              <td class="py-3 px-6">{employee.id}</td>
              <td class="py-3 px-6">{employee.name}</td>
              <td class="py-3 px-6">{employee.role}</td>
              <td 
                class="py-3 px-6 font-bold" 
                class:text-green-500={employee.status === "Active"}
                class:text-red-500={employee.status === "Inactive"}
              >
                {employee.status}
              </td>
              <td class="py-3 px-6">{employee.lastUpdated}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  
  <style>
    /* Add any global styles if necessary */
  </style>
  

