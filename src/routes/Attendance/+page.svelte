<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import Header from '../Header/+page.svelte'; // Import Header component


    let attendanceRecords = [
      {
        attendanceId: 1,
        eventId: "E001",
        participantId: "202210168",
        checkInTime: "2024-12-13 08:00 AM",
        status: "Present",
        notes: "On time",
        createdAt: "2024-12-13 08:00 AM"
      },
      {
        attendanceId: 2,
        eventId: "E001",
        participantId: "202210606",
        checkInTime: "2024-12-13 08:15 AM",
        status: "Absent",
        notes: "No show",
        createdAt: "2024-12-13 08:15 AM"
      }
    ];
  
    let newRecord = {
      eventId: "",
      participantId: "",
      checkInTime: new Date().toISOString().split("T")[0] + " 08:00 AM",
      status: "Present",
      notes: "",
      createdAt: new Date().toISOString().split("T")[0] + " 08:00 AM"
    };
  
    function addRecord() {
      if (newRecord.eventId.trim() && newRecord.participantId.trim()) {
        attendanceRecords = [
          ...attendanceRecords,
          {
            ...newRecord,
            attendanceId: attendanceRecords.length + 1,
          },
        ];
        newRecord = {
          eventId: "",
          participantId: "",
          checkInTime: new Date().toISOString().split("T")[0] + " 08:00 AM",
          status: "Present",
          notes: "",
          createdAt: new Date().toISOString().split("T")[0] + " 08:00 AM"
        };
      }
    }
  </script>

<Header /> <!-- Render the Header component -->
  
  <div class="min-h-screen bg-gray-100 p-6">
    <!-- Page Title -->
    <div class="mb-6 text-center">
      <h1 class="text-3xl font-bold text-gray-800">Attendance</h1>
      <p class="text-gray-600">Mark attendance and view records</p>
    </div>
  
    <!-- Attendance Form -->
    <div class="mb-8 bg-white p-6 rounded-lg shadow-md max-w-3xl mx-auto">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Mark Attendance</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label for="eventId" class="block text-gray-700 font-medium">Event ID</label>
          <input
            id="eventId"
            type="text"
            bind:value={newRecord.eventId}
            placeholder="Enter event ID"
            class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="participantId" class="block text-gray-700 font-medium">Participant ID</label>
          <input
            id="participantId"
            type="text"
            bind:value={newRecord.participantId}
            placeholder="Enter participant ID"
            class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="checkInTime" class="block text-gray-700 font-medium">Check-in Time</label>
          <input
            id="checkInTime"
            type="text"
            bind:value={newRecord.checkInTime}
            placeholder="Enter check-in time"
            class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="status" class="block text-gray-700 font-medium">Status</label>
          <select
            id="status"
            bind:value={newRecord.status}
            class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
        </div>
        <div>
          <label for="notes" class="block text-gray-700 font-medium">Notes</label>
          <textarea
            id="notes"
            bind:value={newRecord.notes}
            placeholder="Enter any notes"
            class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
      </div>
      
      <button
        on:click={addRecord}
        class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
      >
        Add Record
      </button>
    </div>
  
    <!-- Attendance Records Table -->
    <div class="bg-white p-6 rounded-lg shadow-md max-w-4xl mx-auto">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Attendance Records</h2>
      <table class="min-w-full border-collapse">
        <thead class="bg-blue-500 text-white">
          <tr>
            <th class="py-3 px-6 text-left font-semibold">Attendance ID</th>
            <th class="py-3 px-6 text-left font-semibold">Event ID</th>
            <th class="py-3 px-6 text-left font-semibold">Participant ID</th>
            <th class="py-3 px-6 text-left font-semibold">Check-in Time</th>
            <th class="py-3 px-6 text-left font-semibold">Status</th>
            <th class="py-3 px-6 text-left font-semibold">Notes</th>
            <th class="py-3 px-6 text-left font-semibold">Created At</th>
          </tr>
        </thead>
        <tbody>
          {#each attendanceRecords as record (record.attendanceId)}
            <tr class="even:bg-gray-100">
              <td class="py-3 px-6">{record.attendanceId}</td>
              <td class="py-3 px-6">{record.eventId}</td>
              <td class="py-3 px-6">{record.participantId}</td>
              <td class="py-3 px-6">{record.checkInTime}</td>
              <td
                class="py-3 px-6 font-bold"
                class:text-green-500={record.status === "Present"}
                class:text-red-500={record.status === "Absent"}
              >
                {record.status}
              </td>
              <td class="py-3 px-6">{record.notes}</td>
              <td class="py-3 px-6">{record.createdAt}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  
  <style>
    /* Global or additional styles */
  </style>
  
