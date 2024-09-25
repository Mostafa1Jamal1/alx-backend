const createPushNotificationsJobs = function (jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  for (const job of jobs) {
    const Job = queue
      .create('push_notification_code_3', job);
    Job.save(err => {
      if (!err) console.log(`Notification job created: ${Job.id}`);
    });
    Job.on('complete', () => {
      console.log(`Notification job ${Job.id} completed`);
    });
    Job.on('failed', (err) => {
      console.log(`Notification job ${Job.id} failed: ${err}`);
    });
    Job.on('progress', function (progress, data) {
      console.log(`Notification job ${Job.id} ${progress}% complete`);
    });
  }
}

export default createPushNotificationsJobs