
void decode(char *pcParm1,long lParm2)

{
  char cVar1;
  byte bVar2;
  int iVar3;
  uint uVar4;
  size_t sVar5;
  ulong uVar6;
  int iVar7;
  char *pcVar8;
  ulong uVar9;
  int iVar10;
  
  sVar5 = strlen(pcParm1);
  iVar3 = (int)sVar5;
  iVar7 = iVar3 * 5;
  iVar10 = iVar7 + 7;
  if (-1 < iVar7) {
    iVar10 = iVar7;
  }
  iVar10 = iVar10 >> 3;
  if (0 < iVar3) {
    pcVar8 = pcParm1;
    do {
      if (*pcVar8 == padding) {
        *pcVar8 = *table;
      }
      pcVar8 = pcVar8 + 1;
    } while (pcVar8 != pcParm1 + (ulong)(iVar3 - 1) + 1);
  }
  if (0 < iVar10) {
    uVar6 = 0;
    uVar9 = (ulong)(iVar10 - 1) + 1;
LAB_00100c0b:
    do {
      cVar1 = inv_table[(long)*pcParm1];
      bVar2 = inv_table[(long)pcParm1[1]];
      uVar4 = (uint)((uVar6 & 0xffffffff) * 0xcccccccd >> 0x20);
      iVar7 = (int)uVar6 - ((uVar4 >> 2) + (uVar4 & 0xfffffffc));
      if (iVar7 == 2) {
        pcParm1 = pcParm1 + 1;
        *(byte *)(lParm2 + uVar6) = bVar2 >> 1 | cVar1 << 4;
      }
      else {
        if (iVar7 < 3) {
          if (iVar7 == 1) {
            pcVar8 = pcParm1 + 2;
            pcParm1 = pcParm1 + 2;
            *(byte *)(lParm2 + uVar6) = bVar2 * 2 | cVar1 << 6 | (byte)inv_table[(long)*pcVar8] >> 4
            ;
            uVar6 = uVar6 + 1;
            if (uVar6 == uVar9) break;
            goto LAB_00100c0b;
          }
LAB_00100c90:
          pcParm1 = pcParm1 + 1;
          *(byte *)(lParm2 + uVar6) = bVar2 >> 2 | cVar1 << 3;
        }
        else {
          if (iVar7 == 3) {
            pcVar8 = pcParm1 + 2;
            pcParm1 = pcParm1 + 2;
            *(byte *)(lParm2 + uVar6) =
                 bVar2 << 2 | cVar1 << 7 | (byte)inv_table[(long)*pcVar8] >> 3;
          }
          else {
            if (iVar7 != 4) goto LAB_00100c90;
            pcParm1 = pcParm1 + 2;
            *(byte *)(lParm2 + uVar6) = bVar2 | cVar1 << 5;
          }
        }
      }
      uVar6 = uVar6 + 1;
    } while (uVar6 != uVar9);
  }
  *(undefined *)(lParm2 + (long)iVar10) = 0;
  return;
}

