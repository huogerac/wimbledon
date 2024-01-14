import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  // xsrfHeaderName: "X-CSRFToken",
  // xsrfCookieName: "csrftoken",
  // withCredentials: true,
});

export default {
  getCompetitors: async (tournamentId) => {
    const response = await api.get(
      `/api/core/tournaments/${tournamentId}/competitor`
    );
    return response.data;
  },
  getTop4: async (tournamentId) => {
    const response = await api.get(
      `/api/core/tournaments/${tournamentId}/result`
    );
    return response.data;
  },
  getMatches: async (tournamentId) => {
    const response = await api.get(
      `/api/core/tournaments/${tournamentId}/match`
    );
    return response.data;
  },
  saveMatchResult: async (tournamentId, matchId, competitorId) => {
    const response = await api.post(
      `/api/core/tournaments/${tournamentId}/match/${matchId}?winner_competitor_id=${competitorId}`
    );
    return response.data;
  },
};
