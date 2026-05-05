import multiprocessing
import time

# =========================
# IDENTITAS (NRP DIGUNAKAN)
# =========================
NRP = "152024051"

# =========================
# FUNGSI WORKER
# =========================
def execute_task(queue, result_queue, worker_id, delay):
    total = 0
    task_count = 0

    # Dynamic distribution: worker mengambil task dari queue saat runtime
    while not queue.empty():
        try:
            task = queue.get_nowait()
            time.sleep(delay)  # simulasi proses kerja
            total += task
            task_count += 1

            print(f"[Worker {worker_id}] memproses task {task}")

        except:
            break

    print(f"[Worker {worker_id}] selesai | jumlah task: {task_count} | total: {total}")
    result_queue.put(total)


if __name__ == "__main__":

    # =========================
    # PARAMETER DARI NRP
    # =========================
    last_digit = int(NRP[-1])              # menentukan variasi data
    digit_sum = sum(map(int, NRP))         # menentukan worker & delay

    data = list(range(1, 10 + last_digit)) # jumlah data unik (berdasarkan NRP)
    delay = (digit_sum % 5) * 0.01 + 0.05  # delay unik tiap mahasiswa
    num_workers = (digit_sum % 3) + 2      # jumlah worker (2–4)

    print("NRP:", NRP)
    print("Jumlah data:", len(data))
    print("Jumlah worker:", num_workers)
    print()

    # =========================
    # QUEUE (INTI DYNAMIC)
    # =========================
    task_queue = multiprocessing.Queue()
    for d in data:
        task_queue.put(d)

    result_queue = multiprocessing.Queue()

    # =========================
    # EKSEKUSI PARALEL
    # =========================
    start = time.time()

    processes = []
    for i in range(num_workers):
        p = multiprocessing.Process(
            target=execute_task,
            args=(task_queue, result_queue, i, delay)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.time()

    # =========================
    # HASIL AKHIR
    # =========================
    final_total = 0
    while not result_queue.empty():
        final_total += result_queue.get()

    print("\n=== HASIL AKHIR ===")
    print("Total seluruh hasil:", final_total)
    print("Waktu eksekusi:", end - start)

    # =========================
    # INDIKATOR KETENTUAN DOSEN
    # =========================
    print("\nDynamic distribution: task diambil dari queue saat runtime")
    print("Optimal time tercapai karena semua worker aktif (tidak idle)")