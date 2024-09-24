import kue from 'kue';

const queue = kue.createQueue();
const Job = queue.create('push_notification_code', {
  phoneNumber: '1234567890',
  message: 'jon message',
}).save(err => {
  if (!err) console.log(`Notification job created: ${Job.id}`);
});

Job.on('complete', () => {
  console.log('Notification job completed');
}).on('failed', () => {
  console.log('Notification job failed');
})