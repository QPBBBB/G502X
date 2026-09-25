export async function Request(Path, Options = {}) {
  const Response = await fetch(Path, {cache: 'no-store', ...Options});
  const Data = await Response.json();
  if (!Response.ok) throw new Error(Data.Error?.Message || '本机后台请求失败。');
  return Data;
}

export const Discover = () => Request('/Api/Devices');
export const ReadDpi = (Id) => Request(`/Api/Devices/${Id}/Dpi`);
export const SetDpi = (Id, Dpi) => Request(`/Api/Devices/${Id}/Dpi`, {
  method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({Dpi})
});
