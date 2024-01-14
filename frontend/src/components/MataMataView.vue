<template>
  <h1>🏆 Campeonato Mata-Mata 🏆</h1>
  <p class="read-the-docs">by Roger Camargo - 2024</p>

  <!-- ENVIAR-->
  <div v-if="gameWinner && gameId">
    <h2>Enviar resultados:</h2>
    <p>
      Game <strong>{{ gameId }}</strong>
    </p>
    <p>
      Vencedor
      <strong>{{ gameWinner.name }} (id: {{ gameWinner.id }})</strong>
    </p>
    <button type="button" class="btn btn-success" @click="sendSaveMatchResult">
      Enviar <span class="badge text-bg-secondary">🏆</span>
    </button>
  </div>

  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="level of Object.keys(matchesLevel)" :key="level">
        <th scope="row">{{ level }}</th>
        <td>
          <table class="table">
            <tbody>
              <tr v-for="game of matchesLevel[level]" :key="game.id">
                <th scope="row">
                  Game {{ game.game_number }} (id:{{ game.id }})

                  <div
                    class="progress"
                    role="progressbar"
                    aria-label="Animated striped example"
                    aria-valuenow="75"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    v-if="!game.winner"
                  >
                    <div
                      class="progress-bar progress-bar-striped progress-bar-animated"
                      style="width: 100%"
                    ></div>
                  </div>
                </th>
                <td>
                  <button
                    type="button"
                    :class="{
                      btn: true,
                      'btn-primary':
                        game.winner && game.winner.id == game.competitor1.id,
                      'btn-danger':
                        game.winner && game.winner.id != game.competitor1.id,
                      'btn-secondary': !game.winner,
                      'btn-big': true,
                    }"
                    @click="saveMatchResult(game.id, game.competitor1)"
                  >
                    {{ game.competitor1.name }}

                    <span
                      class="badge text-bg-secondary"
                      v-if="
                        game.winner && game.winner.id == game.competitor1.id
                      "
                      >🏆</span
                    >
                  </button>
                  &nbsp;&nbsp;
                  <button
                    type="button"
                    :class="{
                      btn: true,
                      'btn-primary':
                        game.winner && game.winner.id == game.competitor2.id,
                      'btn-danger':
                        game.winner && game.winner.id != game.competitor2.id,
                      'btn-secondary': !game.winner,
                      'btn-big': true,
                    }"
                    @click="saveMatchResult(game.id, game.competitor2)"
                  >
                    {{ game.competitor2.name }}

                    <span
                      class="badge text-bg-secondary"
                      v-if="
                        game.winner && game.winner.id == game.competitor2.id
                      "
                      >🏆</span
                    >
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
  <br /><br />
  <h2>Competidores ({{ competitors.length }})</h2>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Nome</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="competitor of competitors" :key="id">
        <th scope="row">{{ competitor.id }}</th>
        <td>
          {{ competitor.name }}
          <span v-if="top4.length > 0 && top4[0].id == competitor.id"
            >🏅 (1o.)</span
          >
          <span v-if="top4.length > 0 && top4[1].id == competitor.id"
            >🥈 (2o.)</span
          >
          <span v-if="top4.length > 0 && top4[2].id == competitor.id"
            >🥉 (3o.)</span
          >
          <span v-if="top4.length > 0 && top4[3].id == competitor.id">
            (4o.)</span
          >
        </td>
      </tr>
    </tbody>
  </table>

  <br /><br />
  <h2>Top 4</h2>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Nome</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(winner, index) in top4" :key="id">
        <th scope="row">{{ index + 1 }}o.</th>
        <td>
          {{ winner.name }}
          <span v-if="index == 0">🏅</span>
          <span v-if="index == 1">🥈</span>
          <span v-if="index == 2">🥉</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import MatchesApi from "../api/matchesapi.js";

export default {
  setup() {},
  data: () => {
    return {
      tournament: 0,
      matches: [],
      competitors: [],
      top4: [],
      gameId: null,
      gameWinner: null,
    };
  },
  computed: {
    matchesLevel() {
      const ml = {};
      if (!this.matches) return {};
      for (const item of this.matches) {
        const level = item.level_number;
        if (!ml[level]) {
          ml[level] = [];
        }
        ml[level].push(item);
      }
      return ml;
    },
  },
  mounted() {
    const url = new URL(window.location);
    this.tournament = url.searchParams.get("tournament") || 0;
    console.log(`tournament: ${this.tournament}`);
    this.getMatches();
    this.getCompetitors();
    this.getTop4();
  },
  methods: {
    async getMatches() {
      if (!this.tournament) return;
      const response = await MatchesApi.getMatches(this.tournament);
      this.matches = response.matches;
    },
    async getCompetitors() {
      if (!this.tournament) return;
      const response = await MatchesApi.getCompetitors(this.tournament);
      this.competitors = response.competitors;
    },
    async getTop4() {
      if (!this.tournament) return;
      const response = await MatchesApi.getTop4(this.tournament);
      this.top4 = response.competitors;
    },
    async saveMatchResult(gameId, winner) {
      this.gameId = gameId;
      this.gameWinner = winner;
    },
    async sendSaveMatchResult() {
      const response = await MatchesApi.saveMatchResult(
        this.tournament,
        this.gameId,
        this.gameWinner.id
      );
      this.getMatches();
      this.getTop4();
    },
  },
};
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
.btn-big {
  width: 220px;
}
</style>
