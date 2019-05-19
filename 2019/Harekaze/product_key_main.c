
ulong main(int iParm1,undefined8 *puParm2)

{
  char cVar1;
  char *pcVar2;
  int iVar3;
  uint uVar4;
  size_t sVar5;
  char *__s;
  long lVar6;
  int *piVar7;
  int *piVar8;
  ulong uVar9;
  long in_FS_OFFSET;
  byte bVar10;
  int local_68;
  undefined4 uStack100;
  undefined4 uStack96;
  undefined4 uStack92;
  int local_58;
  undefined4 uStack84;
  undefined4 uStack80;
  undefined4 uStack76;
  undefined4 local_48;
  undefined4 uStack68;
  undefined4 uStack64;
  undefined4 uStack60;
  undefined4 local_38;
  undefined4 uStack52;
  undefined4 uStack48;
  undefined4 uStack44;
  undefined local_28;
  long local_20;
  
  bVar10 = 0;
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  local_28 = 0;
  local_48 = 0;
  uStack68 = 0;
  uStack64 = 0;
  uStack60 = 0;
  local_38 = 0;
  uStack52 = 0;
  uStack48 = 0;
  uStack44 = 0;
  local_68 = 0;
  uStack100 = 0;
  uStack96 = 0;
  uStack92 = 0;
  local_58 = 0;
  uStack84 = 0;
  uStack80 = 0;
  uStack76 = 0;
  if (iParm1 < 2) {
    uVar9 = 1;
    __fprintf_chk(stderr,1,"Usage: %s <product key>\n",*puParm2);
  }
  else {
    __s = (char *)puParm2[1];
    sVar5 = strlen(__s);
    if (sVar5 == 0x27) {
      __s = strtok(__s,"-");
      pcVar2 = table;
      while (__s != (char *)0x0) {
        table = pcVar2;
        __strncat_chk(&local_48,__s,4);
        __s = strtok((char *)0x0,"-");
        pcVar2 = table;
      }
      lVar6 = -1;
      __s = pcVar2;
      do {
        uVar4 = (uint)lVar6;
        if (lVar6 == 0) break;
        lVar6 = lVar6 + -1;
        uVar4 = (uint)lVar6;
        cVar1 = *__s;
        __s = __s + (ulong)bVar10 * -2 + 1;
      } while (cVar1 != 0);
      table = pcVar2;
      if (0 < (int)(~uVar4 - 1)) {
        lVar6 = 0;
        table = pcVar2;
        do {
          inv_table[(long)pcVar2[lVar6]] = (char)lVar6;
          lVar6 = lVar6 + 1;
        } while ((ulong)(~uVar4 - 2) + 1 != lVar6);
      }
      decode(&local_48,&local_68);
      iVar3 = 0;
      piVar7 = &local_68;
      do {
        piVar8 = (int *)((long)piVar7 + 1);
        iVar3 = (int)*(char *)piVar7 + iVar3 * 0x1f;
        piVar7 = piVar8;
      } while (&local_58 != piVar8);
      if (local_58 == iVar3) {
        __printf_chk(1,"Hello, %.16s!\n",&local_68);
        uVar4 = strncmp((char *)&local_68,"i-am-misakiakeno",0x10);
        uVar9 = (ulong)uVar4;
        if (uVar4 == 0) {
          __printf_chk(1,"You are admin! The flag is: HarekazeCTF{%s}\n",&local_48);
        }
        else {
          uVar9 = 0;
          puts("You are not admin.");
        }
        goto LAB_0010089f;
      }
    }
    uVar9 = 1;
    fwrite("invalid product key\n",1,0x14,stderr);
  }
LAB_0010089f:
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar9;
}

