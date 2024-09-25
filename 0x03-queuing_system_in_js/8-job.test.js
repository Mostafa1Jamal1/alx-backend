import createPushNotificationsJobs from './8-job.js';
import kue from 'kue';
import chai from 'chai';
import sinon from 'sinon';

const expect = chai.expect;
const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => {
    queue.testMode.enter();
  })
  beforeEach(() => {
    sinon.spy(console, 'log');
  })
  afterEach(() => {
    queue.testMode.clear();
    sinon.restore();
  })
  after(() => {
    queue.testMode.exit();
  })

  it('should create jobs and log them', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(console.log.calledWith('Notification job created: ' + queue.testMode.jobs[0].id)).to.be.true;
    expect(console.log.calledWith('Notification job created: ' + queue.testMode.jobs[1].id)).to.be.true;
  });

  it('should create jobs of type push_notification_code_3 with the correct data', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data.phoneNumber).to.equal('4153518780');
    expect(queue.testMode.jobs[1].data.phoneNumber).to.equal('4153518781');
  });

  it('should display error if jobs is not an array', () => {
    const queue = kue.createQueue();
    expect(function () { createPushNotificationsJobs('jobs', queue) })
      .to.throw(Error, 'Jobs is not an array');
    expect(queue.testMode.jobs.length).to.equal(0);
  });

})