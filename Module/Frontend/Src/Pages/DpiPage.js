import {Discover, ReadDpi, SetDpi} from '../Api/DeviceApi.js';

const Status = document.querySelector('#Status');
const CurrentDpi = document.querySelector('#CurrentDpi');
const Dpi = document.querySelector('#Dpi');
const Range = document.querySelector('#Range');
const Apply = document.querySelector('#Apply');
const Refresh = document.querySelector('#Refresh');
const Message = document.querySelector('#Message');
let Device = null;
let Busy = false;

function SetBusy(Value) {
  Busy = Value;
  Apply.disabled = Value || !Device;
  Dpi.disabled = Value || !Device;
  Refresh.disabled = Value;
}

function ShowMessage(Text, Error = false) {
  Message.textContent = Text;
  Message.dataset.error = String(Error);
}

function Disconnected(Text) {
  Device = null;
  Status.textContent = Text;
  CurrentDpi.textContent = '—';
  Dpi.value = '';
  Dpi.placeholder = '等待设备连接';
  Dpi.setCustomValidity('');
  Range.textContent = '范围与步进将从鼠标读取。';
}

function Render(State, PreserveInput = false) {
  Device = State;
  Status.textContent = `已连接 · ${State.Name}`;
  CurrentDpi.textContent = State.CurrentDpi || '设备未提供';
  Dpi.min = String(State.MinDpi);
  Dpi.max = String(State.MaxDpi);
  Dpi.step = String(State.DpiStep || 1);
  Dpi.placeholder = '输入 DPI';
  if (!PreserveInput) {
    Dpi.value = State.CurrentDpi ? String(State.CurrentDpi) : '';
    Dpi.setCustomValidity('');
  }
  Range.textContent = `${State.MinDpi}–${State.MaxDpi} DPI · ${State.DpiStep ? `步进 ${State.DpiStep}` : '仅接受设备支持的整数值'}`;
}

async function Detect() {
  SetBusy(true);
  Disconnected('正在检查连接…');
  ShowMessage('');
  try {
    const Result = await Discover();
    if (Result.Devices.length === 1) Render(Result.Devices[0]);
    else if (Result.Devices.length > 1) Disconnected('检测到多个 G502 X，请仅保留一个目标接收器后重新检测。');
    else Disconnected(Result.ReceiverCount ? '未连接 · 接收器已插入，鼠标休眠、关闭或不可达。' : '未连接 · 未找到支持的 LIGHTSPEED 接收器。');
    if (!Result.Devices.length && Result.Errors.length) ShowMessage(Result.Errors[0].Message, true);
  } catch (Error) {
    Disconnected('连接状态未知 · 无法完成设备检测。');
    ShowMessage(Error.message, true);
  } finally { SetBusy(false); }
}

document.querySelector('#DpiForm').addEventListener('submit', async Event => {
  Event.preventDefault();
  if (Busy || !Device) return;
  const RequestedDpi = Dpi.valueAsNumber;
  if (!Number.isInteger(RequestedDpi) || !Device.SupportedDpi.includes(RequestedDpi)) {
    Dpi.setCustomValidity('请输入设备支持的整数 DPI，范围和步进见下方提示。');
    Dpi.reportValidity();
    return;
  }
  SetBusy(true);
  ShowMessage('正在应用…');
  try {
    Render(await SetDpi(Device.Id, RequestedDpi));
    ShowMessage(`已应用 ${Device.CurrentDpi} DPI，并完成读回确认。`);
  } catch (Error) {
    Disconnected('连接状态待确认 · 请重新检测。');
    ShowMessage(`${Error.message} 若请求已发送，设置可能已生效，请重新检测。`, true);
  } finally { SetBusy(false); }
});
Refresh.addEventListener('click', Detect);
Dpi.addEventListener('input', () => Dpi.setCustomValidity(''));
// 串行轮询当前设备；断连后保留提示，由用户重新检测，避免持续扫描。
setInterval(async () => {
  if (Busy || !Device || document.hidden) return;
  // 读取期间保留输入框的可编辑状态，避免打断输入。
  Busy = true;
  Apply.disabled = true;
  Refresh.disabled = true;
  try { Render(await ReadDpi(Device.Id), true); }
  catch (Error) { Disconnected('未连接 · 鼠标不可达，或后台服务已停止。'); ShowMessage(Error.message, true); }
  finally { SetBusy(false); }
}, 5000);
Detect();
