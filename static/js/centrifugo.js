const container = document.getElementsByClassName('answer-container')[0];

const centrifuge = new Centrifuge(container.dataset.wsUrl, {
    token: container.dataset.token
});

centrifuge.on('connecting', function (ctx) {
  console.log(`connecting: ${ctx.code}, ${ctx.reason}`);
}).on('connected', function (ctx) {
  console.log(`connected over ${ctx.transport}`);
}).on('disconnected', function (ctx) {
  console.log(`disconnected: ${ctx.code}, ${ctx.reason}`);
}).connect();

const sub = centrifuge.newSubscription(container.dataset.questionId);

sub.on('publication', function (ctx) {
    const answerTemplate = document.getElementById("answer-template");
    let templateHTML = answerTemplate.innerHTML;
    templateHTML = templateHTML
        .replace(/%% answer_id %%/g, ctx.data.answer_id)
        .replace(/%% avatar_url %%/g, ctx.data.avatar_url)
        .replace(/%% author %%/g, ctx.data.author)
        .replace(/%% text %%/g, ctx.data.text)
        .replace(/%% votes_total %%/g, ctx.data.votes_total)
        .replace(/%% question_id %%/g, ctx.data.question_id)

    const tempDiv = document.createElement("div");
    tempDiv.className = "row";
    tempDiv.innerHTML = templateHTML;
    container.prepend(tempDiv);
}).on('subscribing', function (ctx) {
  console.log(`subscribing: ${ctx.code}, ${ctx.reason}`);
}).on('subscribed', function (ctx) {
  console.log('subscribed', ctx);
}).on('unsubscribed', function (ctx) {
  console.log(`unsubscribed: ${ctx.code}, ${ctx.reason}`);
}).subscribe();